import hashlib
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, asdict, field
from os import PathLike
from typing import List, Dict, Any, Optional

import jinja2


def _escape(string: str):
    def replace(match: re.Match):
        return "%" + "".join("%{:02X}".format(c) for c in match.group(1).encode())

    return re.sub(r"([^a-zA-Z0-9_.\-~+]+)", replace, string)


@dataclass
class Package:
    name: str
    version: str
    filename: Optional[str] = field(repr=False)
    epoch: Optional[str] = field(repr=False)
    iteration: Optional[str] = field(repr=False)
    maintainer: Optional[str] = field(repr=False)
    vendor: Optional[str] = field(repr=False)
    url: Optional[str] = field(repr=False)
    category: Optional[str] = field(repr=False)
    license: Optional[str] = field(repr=False)
    architecture: Optional[str] = field(repr=False)
    description: Optional[str] = field(repr=False)
    dependencies: Optional[List[str]] = field(repr=False)
    sha1: Optional[str] = field(repr=False)
    sha256: Optional[str] = field(repr=False)
    md5: Optional[str] = field(repr=False)
    size: Optional[str] = field(repr=False)
    _url_filename: Optional[str] = field(repr=False)
    attributes: Dict[str, Any] = field(repr=False)

    @property
    def full_version(self):
        if all(v is None for v in [self.epoch, self.version, self.iteration]):
            return None

        combined_version = ":".join(filter(None, [self.epoch, self.version]))
        return (
            f"{combined_version}-{self.iteration}"
            if self.iteration
            else combined_version
        )

    def url_filename(self, codename: str):
        if self._url_filename is not None:
            return self._url_filename
        if self.filename:
            return f"pool/{codename}/{self.name[0]}/{self.name[:2]}/{os.path.basename(self.filename)}"

    def url_filename_encoded(self, codename: str):
        if self._url_filename is not None:
            return self._url_filename
        if self.filename:
            return f"pool/{codename}/{self.name[0]}/{self.name[:2]}/{_escape(os.path.basename(self.filename))}"

    @classmethod
    def parse_file(cls, filename: PathLike):
        control_data = cls.parse_control(cls.extract_control(filename))
        file_info_data = cls.parse_file_info(filename)
        package = cls(**{"filename": filename, **control_data, **file_info_data})
        return package

    @classmethod
    def parse_string(cls, string: str):
        control_data = cls.parse_control(string)
        package = cls(filename=None, **control_data)
        return package

    @staticmethod
    def extract_control(filename: PathLike) -> str:
        try:
            subprocess.run(
                ["which", "dpkg"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            control_data = subprocess.check_output(["dpkg", "-f", filename]).decode(
                "utf-8"
            )
        except subprocess.CalledProcessError:
            package_files = subprocess.check_output(["ar", "t", filename]).decode(
                "utf-8"
            )
            control_filename = next(
                fname
                for fname in package_files.split("\n")
                if fname.startswith("control.")
            )
            compression = "z" if control_filename == "control.tar.gz" else "J"

            extract_control_tarball_cmd = f"ar p {filename} {control_filename}"

            try:
                subprocess.run(
                    ["ar", "t", filename, control_filename],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                )
            except subprocess.CalledProcessError:
                print("Failed to find control data in .deb with ar, trying tar.")
                extract_control_tarball_cmd = (
                    f"tar {compression}xf {filename} --to-stdout {control_filename}"
                )

            with tempfile.TemporaryDirectory() as path:
                extract_cmd = (
                    f"{extract_control_tarball_cmd} | tar -{compression}xf - -C {path}"
                )
                subprocess.run(extract_cmd, shell=True, check=True)
                with open(
                    os.path.join(path, "control"), "r", encoding="utf-8"
                ) as control_file:
                    control_data = control_file.read()

        return control_data

    @classmethod
    def parse_control(cls, control) -> Dict[str, Any]:
        # Gather fields in control file
        fields = {}
        for line in control.splitlines():
            field = None
            value = ""
            if match := re.match(r"^(\s+)(\S.*)$", line):
                indent = match.group(1)
                rest = match.group(2)

                if len(indent) == 1 and rest == ".":
                    value += "\n"
                    rest = ""
                elif len(value) > 0:
                    value += "\n"

                value += rest
            elif match := re.match(r"^([-\w]+):(.*)$", line):
                if field:
                    fields[field] = value

                field = match.group(1)
                value = match.group(2).strip()

            if field:
                fields[field] = value

        # Packages manifest fields
        data = {}

        # Parse 'epoch:version-iteration' in the version string
        full_version = fields.pop("Version")
        version_match = re.match(r"^(?:([0-9]+):)?(.+?)(?:-(.*))?$", full_version)
        if not version_match:
            raise ValueError(f"Unsupported version string '{full_version}'")

        epoch, version, iteration = version_match.groups()
        data["epoch"] = epoch
        data["version"] = version
        data["iteration"] = iteration

        data["architecture"] = fields.pop("Architecture", None)
        data["category"] = fields.pop("Section", None)
        data["license"] = fields.pop("License", None) or "unknown"
        data["maintainer"] = fields.pop("Maintainer", None)
        data["name"] = fields.pop("Package", None)
        data["url"] = fields.pop("Homepage", None)
        data["vendor"] = fields.pop("Vendor", None) or "none"
        data["_url_filename"] = fields.pop("Filename", None)
        data["sha1"] = fields.pop("SHA1", None)
        data["sha256"] = fields.pop("SHA256", None)
        data["md5"] = fields.pop("MD5sum", None)
        data["size"] = fields.pop("Size", None)
        data["description"] = fields.pop("Description", None)
        data["dependencies"] = cls.parse_depends(fields.pop("Depends", None))

        # other attributes
        attributes: Dict[str, Any] = {}
        attributes["deb_priority"] = fields.pop("Priority", None)
        attributes["deb_origin"] = fields.pop("Origin", None)
        attributes["deb_installed_size"] = fields.pop("Installed-Size", None)
        attributes["deb_recommends"] = fields.pop("Recommends", None)
        attributes["deb_suggests"] = fields.pop("Suggests", None)
        attributes["deb_enhances"] = fields.pop("Enhances", None)
        attributes["deb_pre_depends"] = fields.pop("Pre-Depends", None)
        attributes["deb_breaks"] = fields.pop("Breaks", None)
        attributes["deb_conflicts"] = fields.pop("Conflicts", None)
        attributes["deb_provides"] = fields.pop("Provides", None)
        attributes["deb_replaces"] = fields.pop("Replaces", None)
        attributes["deb_field"] = {k.split("-", 1)[-1]: v for k, v in fields.items()}
        data["attributes"] = attributes

        return data

    @staticmethod
    def parse_depends(data):
        if data is None or not data:
            return []

        # parse dependencies. Debian dependencies come in one of two forms:
        # * name
        # * name (op version)
        # They are all on one line, separated by ", "

        dep_re = re.compile(r"^([^ ]+)(?: \(([>=<]+) ([^)]+)\))?$")
        dependencies = []

        for dep in re.split(r", *", data):
            m = dep_re.match(dep)
            if m:
                name, op, version = m.groups()
                # this is the proper form of dependency
                if op and version and op != "" and version != "":
                    dependencies.append(f"{name} ({op} {version})".strip())
                else:
                    dependencies.append(name.strip())
            else:
                # Assume normal form dependency, "name op version".
                dependencies.append(dep)

        return dependencies

    @staticmethod
    def parse_file_info(filename: PathLike):
        data: Dict[str, Any] = {}
        data["size"] = os.path.getsize(filename)

        with open(filename, "rb") as f:
            content = f.read()
            data["sha1"] = hashlib.sha1(content).hexdigest()
            data["sha256"] = hashlib.sha256(content).hexdigest()
            data["md5"] = hashlib.md5(content).hexdigest()

        return data

    def generate(self, codename: str):
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("dpkgs3"),
            autoescape=jinja2.select_autoescape(),
        )
        template = env.get_template("package.jinja2")
        return template.render(
            **asdict(self),
            url_filename_encoded=self.url_filename_encoded(codename),
        )
