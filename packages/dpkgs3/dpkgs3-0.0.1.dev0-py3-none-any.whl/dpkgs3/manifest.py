import gzip
import hashlib
import os
import tempfile
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional

from dpkgs3.package import Package
from dpkgs3.s3 import S3


@dataclass
class Manifest:
    codename: str
    component: str
    architecture: str
    packages: List[Package] = field(default_factory=list, repr=False)
    packages_to_be_uploaded: List[Package] = field(default_factory=list, repr=False)
    files: Dict[str, str] = field(default_factory=dict, repr=False)
    cache_control: str = field(default="", repr=False)
    fail_if_exists: bool = field(default=False, repr=False)
    skip_package_upload: bool = field(default=False, repr=False)

    @classmethod
    def retrieve(
        cls, s3: S3, codename: str, component: str, architecture: str, **kwargs
    ):
        m = cls(
            codename,
            component,
            architecture,
            **kwargs,
        )
        packages_data = s3.read(
            f"dists/{codename}/{component}/binary-{architecture}/Packages"
        )
        if packages_data is not None:
            m.packages = cls.parse_packages(packages_data.decode("utf-8"))

        return m

    @staticmethod
    def parse_packages(packages_data: str) -> List[Package]:
        packages = []
        for s in packages_data.split("\n\n"):
            if s.rstrip():
                packages.append(Package.parse_string(s))
        return packages

    def add_package(
        self,
        pkg: Package,
        preserve_versions: bool = True,
        fail_if_exists: bool = True,
        needs_uploading: bool = True,
    ):
        if fail_if_exists:
            for p in self.packages:
                if (
                    p.name == pkg.name
                    and p.full_version == pkg.full_version
                    and os.path.basename(p.url_filename(self.codename))
                    == os.path.basename(pkg.url_filename(self.codename))
                ):
                    raise Exception(
                        f"package {pkg.name}_{pkg.full_version} already exists with filename ({p.url_filename(self.codename)})"
                    )

        self.packages = [
            p
            for p in self.packages
            if not (
                p.name == pkg.name
                and (p.full_version == pkg.full_version if preserve_versions else True)
            )
        ]
        self.packages.append(pkg)
        if needs_uploading:
            self.packages_to_be_uploaded.append(pkg)

        return pkg

    def delete_package(
        self,
        pkg_name: str,
        versions: Optional[List[str]] = None,
    ):
        deleted_packages = []
        versions = versions if versions is not None else []
        for p in self.packages:
            if p.name == pkg_name and any(
                [
                    possible_version in versions
                    for possible_version in [
                        p.version,
                        p.full_version,
                        f"{p.version}-{p.iteration}",
                    ]
                ]
            ):
                deleted_packages.append(p)

        self.packages = list(set(self.packages) - set(deleted_packages))
        return deleted_packages

    def generate(self):
        return "\n".join([package.generate(self.codename) for package in self.packages])

    def write_to_s3(self, s3: S3):
        manifest = self.generate()

        if not self.skip_package_upload:
            for pkg in self.packages_to_be_uploaded:
                assert pkg.filename is not None
                s3.store(
                    pkg.filename,
                    pkg.url_filename(self.codename),
                    "application/x-debian-package",
                    self.cache_control,
                    fail_if_exists=self.fail_if_exists,
                )

        # generate the Packages file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as pkgs_temp:
            pkgs_temp.write(manifest)
            pkgs_temp.close()
            f = f"dists/{self.codename}/{self.component}/binary-{self.architecture}/Packages"
            s3.store(pkgs_temp.name, f, "text/plain; charset=utf-8", self.cache_control)
            self.files[
                f"{self.component}/binary-{self.architecture}/Packages"
            ] = self.hashfile(pkgs_temp.name)
            os.unlink(pkgs_temp.name)

        # generate the Packages.gz file
        with tempfile.NamedTemporaryFile(delete=False) as gztemp:
            gztemp.close()
            with gzip.open(gztemp.name, "wb") as gz:
                gz.write(manifest.encode("utf-8"))
            f = f"dists/{self.codename}/{self.component}/binary-{self.architecture}/Packages.gz"
            s3.store(gztemp.name, f, "application/x-gzip", self.cache_control)
            self.files[
                f"{self.component}/binary-{self.architecture}/Packages.gz"
            ] = self.hashfile(gztemp.name)
            os.unlink(gztemp.name)

    @staticmethod
    def hashfile(path: str):
        data: Dict[str, Any] = {}
        data["size"] = os.path.getsize(path)

        with open(path, "rb") as f:
            content = f.read()
            data["sha1"] = hashlib.sha1(content).hexdigest()
            data["sha256"] = hashlib.sha256(content).hexdigest()
            data["md5"] = hashlib.md5(content).hexdigest()

        return data
