import datetime
import os
import re
import tempfile
from dataclasses import dataclass, asdict, field
from typing import Any, List, Union, Dict, Optional

import jinja2
from dpkgs3.s3 import S3
from dpkgs3.manifest import Manifest


@dataclass
class Release:
    codename: str
    origin: Optional[str] = field(default=None, repr=False)
    suite: Optional[str] = field(default=None, repr=False)
    architectures: List[str] = field(default_factory=list, repr=False)
    components: List[str] = field(default_factory=list, repr=False)
    cache_control: Optional[str] = field(default=None, repr=False)
    files: Dict[str, Any] = field(default_factory=dict, repr=False)
    access_policy: str = field(default="public-read", repr=False)

    @classmethod
    def retrieve(
        cls,
        s3: S3,
        codename: str,
        origin: Optional[str] = None,
        suite: Union[str, None] = None,
        cache_control: Union[str, None] = None,
    ):
        release_data = s3.read(f"dists/{codename}/Release")
        if release_data is not None:
            rel = cls.parse_release(release_data.decode("utf-8"))
        else:
            rel = cls(codename=codename)

        rel.codename = codename
        rel.origin = origin if origin is not None else rel.origin
        rel.suite = suite if suite is not None else rel.suite
        rel.cache_control = cache_control

        return rel

    @classmethod
    def parse_release(cls, release_data: str):
        lines = release_data.split("\n")

        def parse_field(field):
            value = next(
                (
                    line.split(": ", 1)[1]
                    for line in lines
                    if line.startswith(field + ": ")
                ),
                None,
            )
            return value

        # Initialize variables to None or empty lists/dicts
        codename = parse_field("Codename")
        origin = parse_field("Origin")
        suite = parse_field("Suite")
        architectures = re.findall(r"^Architectures: (.+)", release_data, re.MULTILINE)
        architectures = architectures[0].split() if architectures else []
        components = re.findall(r"^Components: (.+)", release_data, re.MULTILINE)
        components = components[0].split() if components else []

        files: Dict[str, Any] = {}

        # Find all the hashes
        hashes = re.findall(r"^\s+([^\s]+)\s+(\d+)\s+(.+)$", release_data, re.MULTILINE)
        for hash, size, name in hashes:
            if name in files:
                files[name].update({"size": int(size)})
            else:
                files[name] = {"size": int(size)}

            if len(hash) == 32:
                files[name]["md5"] = hash
            elif len(hash) == 40:
                files[name]["sha1"] = hash
            elif len(hash) == 64:
                files[name]["sha256"] = hash

        return cls(
            codename=codename,
            origin=origin,
            suite=suite,
            architectures=architectures,
            components=components,
            files=files,
        )

    def update_manifest(self, manifest: Manifest):
        if manifest.component not in self.components:
            self.components.append(manifest.component)
        if manifest.architecture not in self.architectures:
            self.architectures.append(manifest.architecture)
        self.files.update(manifest.files)

    def validate_others(self):
        to_apply = []
        for comp in self.components:
            for arch in ["amd64", "i386", "armhf"]:
                if f"{comp}/binary-{arch}/Packages" not in self.files:
                    m = Manifest(
                        codename=self.codename, component=comp, architecture=arch
                    )
                    m.write_to_s3()
                    to_apply.append(m)

        for m in to_apply:
            self.update_manifest(m)

    def generate(self):
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("dpkgs3"),
            autoescape=jinja2.select_autoescape(),
        )
        template = env.get_template("release.jinja2")
        return template.render(
            **asdict(self),
            now=datetime.datetime.now()
            .astimezone(datetime.timezone.utc)
            .strftime("%a, %d %b %Y %T %Z"),
        )

    def write_to_s3(self, s3: S3):
        self.validate_others()

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as release_tmp:
            release_tmp.write(self.generate())
            release_tmp.close()

            s3.store(
                release_tmp.name,
                f"dists/{self.codename}/Release",
                "text/plain; charset=utf-8",
                self.cache_control,
            )

            # TODO: gpg signing key

            os.unlink(release_tmp.name)
