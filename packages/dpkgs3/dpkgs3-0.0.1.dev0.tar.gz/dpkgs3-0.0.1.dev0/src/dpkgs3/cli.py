import os
from pathlib import Path
from typing import Dict, List, Optional

import click
from dpkgs3.s3 import S3
from dpkgs3.release import Release
from dpkgs3.manifest import Manifest
from dpkgs3.package import Package


def configure_s3_client(
    s3_bucket: str,
    s3_prefix: Optional[str],
    s3_visibility: str,
    s3_encryption: bool,
    aws_default_region: Optional[str],
    aws_access_key_id: Optional[str],
    aws_secret_access_key: Optional[str],
):
    if aws_default_region is not None:
        os.environ.setdefault("AWS_DEFAULT_REGION", aws_default_region)
    if aws_access_key_id is not None:
        os.environ.setdefault("AWS_ACCESS_KEY_ID", aws_access_key_id)
    if aws_secret_access_key is not None:
        os.environ.setdefault("AWS_SECRET_ACCESS_KEY", aws_secret_access_key)

    s3 = S3(
        bucket=s3_bucket,
        prefix=s3_prefix,
        access_policy=s3_visibility,
        encryption=s3_encryption,
    )
    return s3


def add_common_options():
    common_options = [
        click.option(
            "--codename",
            default="stable",
            show_default=True,
            help="The codename of the APT repository",
        ),
        click.option(
            "--component",
            default="main",
            show_default=True,
            help="The component of the APT repository",
        ),
        click.option("--s3-bucket", required=True, help="S3 bucket name"),
        click.option(
            "--s3-prefix",
            default="",
            show_default=True,
            help="Path prefix to use when storing on S3",
        ),
        click.option(
            "--s3-visibility",
            type=click.Choice(
                choices=[
                    "public-read",
                    "private",
                    "authenticated-read",
                    "bucket-owner-full-control",
                ]
            ),
            default="public-read",
            show_default=True,
            help="The access policy for the uploaded files",
        ),
        click.option(
            "--s3-encryption",
            is_flag=True,
            default=False,
            show_default=True,
            help="Use S3 server side encryption",
        ),
        click.option("--aws-default-region", default=None, help="AWS default region"),
        click.option("--aws-access-key-id", default=None, help="AWS Access Key ID"),
        click.option(
            "--aws-secret-access-key", default=None, help="AWS Secret Access Key"
        ),
    ]

    def inner(func):
        for option in reversed(common_options):
            func = option(func)
        return func

    return inner


@click.group()
def cli(**kwargs):
    pass


@cli.command()
@add_common_options()
@click.option(
    "--preserve-versions",
    is_flag=True,
    default=True,
    show_default=True,
    help="Whether to preserve other versions of a package in the repository when uploading one",
)
@click.option(
    "--cache-control", default="", help="Cache-Control headers to add to S3 objects"
)
@click.option(
    "--fail-if-exists",
    is_flag=True,
    default=False,
    show_default=True,
    help="Whether to preserve other versions of a package in the repository when uploading one",
)
@click.option(
    "--skip-package-upload",
    is_flag=True,
    default=False,
    show_default=True,
    help="Whether to skip all package uploads. This is useful when hosting .deb outside of the bucket.",
)
@click.argument(
    "files", nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
def upload(
    files: List[Path],
    codename: str,
    component: str,
    preserve_versions: bool,
    cache_control: str,
    fail_if_exists: bool,
    skip_package_upload: bool,
    s3_bucket: str,
    s3_prefix: str,
    s3_visibility: str,
    s3_encryption: bool,
    aws_default_region: Optional[str],
    aws_access_key_id: Optional[str],
    aws_secret_access_key: Optional[str],
):
    if len(files) == 0:
        raise click.MissingParameter(param_type="argument", param_hint="FILES")

    for filename in files:
        _, ext = os.path.splitext(filename)
        if ext != ".deb":
            raise click.BadParameter(
                param_hint="FILES", message=f"{filename} is not a .deb file"
            )

    s3 = configure_s3_client(
        s3_bucket,
        s3_prefix,
        s3_visibility,
        s3_encryption,
        aws_default_region,
        aws_access_key_id,
        aws_secret_access_key,
    )

    print("Retrieving existing manifests")
    release = Release.retrieve(
        s3=s3,
        codename=codename,
        cache_control=cache_control,
    )
    manifests: Dict[str, Manifest] = {}
    for arch in release.architectures:
        manifests[arch] = Manifest.retrieve(
            s3=s3,
            codename=codename,
            component=component,
            architecture=arch,
            cache_control=cache_control,
            skip_package_upload=skip_package_upload,
        )

    for filename in files:
        pkg = Package.parse_file(filename)
        manifest = manifests[pkg.architecture]
        print(f"Add package file {filename} to {manifest}")
        try:
            manifest.add_package(
                pkg, preserve_versions=preserve_versions, fail_if_exists=fail_if_exists
            )
        except Exception as e:
            raise click.ClickException(str(e))

    for manifest in manifests.values():
        if len(manifest.packages_to_be_uploaded) > 0:
            print(f"Uploading packages in {manifest}")
            manifest.write_to_s3(s3=s3)

    print("Updating Release file")
    release.write_to_s3(s3=s3)

    print("Update complete.")
