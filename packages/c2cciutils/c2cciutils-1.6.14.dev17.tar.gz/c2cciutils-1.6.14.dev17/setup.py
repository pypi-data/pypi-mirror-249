# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['c2cciutils', 'c2cciutils.lib', 'c2cciutils.scripts', 'c2cciutils.scripts.k8s']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.0.0,<4.0.0',
 'PyYAML>=6.0.0,<7.0.0',
 'cryptography>=41.0.0,<42.0.0',
 'debian-inspector>=31.0.0,<32.0.0',
 'defusedxml>=0.0.0,<1.0.0',
 'markdown-table>=2020.0.0,<2021.0.0',
 'python-magic>=0.0.0,<1.0.0',
 'requests>=2.0.0,<3.0.0',
 'ruamel.yaml>=0.0.0,<1.0.0',
 'toml>=0.0.0,<1.0.0',
 'urllib3>=2.0.0,<3.0.0']

extras_require = \
{'pr_checks': ['codespell==2.2.6'],
 'publish': ['google-api-python-client>=2.0.0,<3.0.0',
             'google-auth-httplib2>=0.0.0,<1.0.0',
             'google-auth-oauthlib>=1.0.0,<2.0.0',
             'twine>=4.0.0,<5.0.0',
             'tomlkit>=0.0.0,<1.0.0'],
 'version': ['multi-repo-automation>=0.0.0,<1.0.0']}

entry_points = \
{'console_scripts': ['c2cciutils = c2cciutils.scripts.main:main',
                     'c2cciutils-audit = c2cciutils.scripts.audit:main',
                     'c2cciutils-checks = c2cciutils.scripts.env:main',
                     'c2cciutils-clean = c2cciutils.scripts.clean:main',
                     'c2cciutils-docker-logs = '
                     'c2cciutils.scripts.docker_logs:main',
                     'c2cciutils-docker-versions-gen = '
                     'c2cciutils.scripts.docker_versions_gen:main',
                     'c2cciutils-docker-versions-update = '
                     'c2cciutils.scripts.docker_versions_update:main',
                     'c2cciutils-download-applications = '
                     'c2cciutils.scripts.download_applications:main',
                     'c2cciutils-env = c2cciutils.scripts.env:main',
                     'c2cciutils-google-calendar = '
                     'c2cciutils.publish:main_calendar',
                     'c2cciutils-k8s-db = c2cciutils.scripts.k8s.db:main',
                     'c2cciutils-k8s-install = '
                     'c2cciutils.scripts.k8s.install:main',
                     'c2cciutils-k8s-logs = c2cciutils.scripts.k8s.logs:main',
                     'c2cciutils-k8s-wait = c2cciutils.scripts.k8s.wait:main',
                     'c2cciutils-pin-pipenv = '
                     'c2cciutils.scripts.pin_pipenv:main',
                     'c2cciutils-publish = c2cciutils.scripts.publish:main',
                     'c2cciutils-pull-request-checks = '
                     'c2cciutils.scripts.pr_checks:main',
                     'c2cciutils-trigger-image-update = '
                     'c2cciutils.scripts.trigger_image_update:main',
                     'c2cciutils-version = c2cciutils.scripts.version:main']}

setup_kwargs = {
    'name': 'c2cciutils',
    'version': '1.6.14.dev17',
    'description': 'Common utilities for Camptocamp CI',
    'long_description': '# C2C CI utils\n\n## Publishing\n\nThe main goals of C2C CI utils is to offer the commands and the workflows to have the following project structure:\n\nHave stabilization branches named by default `<major>.<minor>`.\nHave the release named by default `<major>.<minor>.<patch>`.\n\nWith C2C CI utils you can publish a python package and a Docker image from the same repository.\n\nThe default publishing are:\n\n- Push on the `<major>.<minor>` branch will publish Docker images.\n- Create the tag `<major>.<minor>.<patch>` will publish the Docker images, and the Python package.\n- Push on a feature branch (whatever other name) will publish the Docker images.\n- Delete a feature branch will delete the Docker images.\n- Push on the `master` branch will publish the Docker images with the master tag (Publishing a python package is also possible).\n- The version at the last line of the `SECURITY.md` of the `master` branch will be also published using the `latest` tag,\n  this will respect the `tags` present in the configuration\n- In the `SECURITY.md` file of the `master` branch we can also add a column `Alternate Tag` to publish the Docker images with another tag,\n  this will respect the `tags` present in the configuration (only for Docker).\n\nThe Docker images are published on Docker Hub and GitHub Container Registry.\n\nYou can run the publishing locally in dry-run mode:\n\n```bash\nGITHUB_REF=... c2cciutils-publish --dry-run ...\n```\n\n## Changelog\n\nWhen we create a tag by default with the `changelog` workflow a release is created on GitHub, a changelog is\ngenerated and added to the release.\n\n## Security\n\nThe security is managed by the `c2cciutils-audit` command with Snyk, it will audit the dependencies of the project on every\nstabilization branches, if possible a pull request is created automatically to update the dependencies.\n\nWhen we publish a Docker image the generated image is monitored by Snyk, this means that Snyk will search\nfor all the dependencies and send the list to the Snyk web site to be monitored.\nWe also do a test of the image and log the result (This will never cause the build to fail).\n\n## Checks\n\nC2C CI utils will no more provide a tool to do a check of the project, this is replaced by `pre-commit`,\na base configuration is provided in the example project.\n\n## Pull request checks\n\nA workflow is provided to run the checks on the pull requests, it will run the `c2cciutils-pr-checks` command.\n\n- Check that the commit message and the pull request title start with a capital letter.\n- Check that there aren\'t any spelling issue in the commit message and in the pull request title.\n- Add a message to the pull request with a link to the JIRA issue if the pull request branch name starts with\n  `[a-zA-Z]+-[0-9]+-` or end with `-[a-zA-Z]+-[0-9]+`.\n\n## Dependencies\n\nIn the example project there is a basic Renovate configuration, it will update the dependencies of the project.\nThere is also a workflow to add a review on the Renovate pull requests to make the auto merge working on\nrepository that required a review.\n\n## Backports\n\nA workflow is provided to backport the pull requests on the stabilization branches, it will be triggered by\nadding a label named `backport <destination_branch>` on the pull request.\n\n## Old workflows\n\nGitHub will retain all the old workflows, so we need to delete them, the `delete-old-workflows-run`\nworkflow will delete the workflows older than 500 days.\n\n## Workflows\n\nC2cciutils make easier to have those workflows in a project:\n\n- `audit.yaml`: Audit the stabilization branches of the application against vulnerabilities in the python and node dependency\n- `auto-review.yaml`: Auto review the Renovate pull requests\n- `backport.yaml`: Trigger the backports (work with labels)\n- `clean.yaml`: Clean the Docker images related on a deleted feature branch\n- `main.yaml`: Main workflow especially with the c2cciutils-checks command\n- `changelog.yaml`: Generate the changelog and create the release on GitHub\n- `delete-old-workflows-run.yaml`: Delete the old workflows\n- `pr-checks.yaml`: Run the checks on the pull requests\n\nAll the provided commands used in the workflow:\n\n- `c2cciutils`: some generic tools.\n- `c2cciutils-version`: Create a new version of the project.\n- `c2cciutils-checks`: Run the checks on the code (those checks don\'t need any project dependencies).\n- `c2cciutils-audit`: Do the audit, the main difference with checks is that it can change between runs on the same code.\n- `c2cciutils-publish`: Publish the project.\n- `c2cciutils-clean`: Delete Docker images on Docker Hub after corresponding branch have been deleted.\n\n## Utilities\n\nThe following utilities are provided:\n\n- `c2cciutils`: some generic tools.\n- `c2cciutils-download-applications`: Download the applications with version managed by Renovate, see below.\n- `c2cciutils-docker-logs`: Display the logs of the application in Docker (compose).\n- `c2cciutils-k8s-install`: Install a k3d / k3s cluster, see below.\n- `c2cciutils-k8s-logs`: Display the logs of the application in the k8s cluster, see below.\n- `c2cciutils-k8s-db`: Create a database in the k8s cluster, see below.\n- `c2cciutils-k8s-wait`: Wait that the application started correctly in the cluster, see below.\n- `c2cciutils-docker-versions-gen`: Generate the Docker package versions file (`ci/dpkg-versions.yaml`), see below.\n- `c2cciutils-pin-pipenv`: Display all the dependencies that\'s in the `Pipenv.lock` but not in the `Pipenv` to be able to pin them.\n- `c2cciutils-trigger-image-update`: Trigger the ArgoCD repository about image update on the CI (automatically done in the publishing).\n- `c2cciutils-google-calendar`: Tool to test the Google credentials for calendar API and refresh them if needed. See `c2cciutils-google-calendar -h` for more information.\n\n## New project\n\nThe content of `example-project` can be a good base for a new project.\n\n## New version\n\nRequirements: the right version (>= 1.6) of `c2cciutils` should be installed with the `version` extra.\n\nTo create a new minor version you just should run `c2cciutils-version --version=<version>`.\n\nYou are welcome to run `c2cciutils-version --help` to see what\'s it\'s done.\n\nNote that it didn\'t create a tag, you should do it manually.\n\nTo create a patch version you should just create tag.\n\n## Secrets\n\nIn the CI we need to have the following secrets::\n\n- `HAS_SECRETS` to be set to \'HAS_SECRETS\', to avoid error errors from external\n  pull requests, already set globally on Camptocamp organization.\n- `GOPASS_CI_GITHUB_TOKEN` and `CI_GPG_PRIVATE_KEY` required to initialize the gopass password store,\n  the secrets exists in the Camptocamp organization but not shared on all project, then you should add\n  your project to the shared list.\n\n## Use locally, in the projects that use c2cciutils\n\nInstall it: `python3 -m pip install --user --requirement ci/requirements.txt`\nDry run publish: `GITHUB_REF=... c2cciutils-publish --dry-run ...`\n\n## Configuration\n\nYou can get the current configuration with `c2cciutils --get-config`, the default configuration depends on your project.\nNote that it didn\'t contain the default defined the schema and visible in the [generated documentation](./config.md).\n\nYou can override the configuration with the file `ci/config.yaml`.\n\nAt the base of the configuration you have:\n\n- `version`: Contains some regular expressions to find the versions branches and tags, and to convert them into application versions.\n- `audit`: The audit configuration, see `c2cciutils/audit.py` for more information.\n- `publish`: The publishing configuration, see `c2cciutils/publish.py` for more information.\n\nMany actions can be disabled by setting the corresponding configuration part to `False`.\n\n## SECURITY.md\n\nThe `SECURITY.md` file should contain the security policy of the repository, especially the end of\nsupport dates.\n\nFor compatibility with `c2cciutils` it should contain an array with at least the columns\n`Version` and `Supported Until`. The `Version` column will contain the concerned version.\nThe `Supported Until` will contain the date of end of support `dd/mm/yyyy`.\nIt can also contain the following sentences:\n\n- `Unsupported`: no longer supported => no audit, no rebuild.\n- `Best effort`: the support is ended, it is still rebuilt and audited, but this can be stopped without any notice.\n- `To be defined`: not yet released or the date will be set related of another project release date (like for GeoMapFish).\n\nSee also [GitHub Documentation](https://docs.github.com/en/github/managing-security-vulnerabilities/adding-a-security-policy-to-your-repository)\n\n## IDE\n\nThe IDE should be configured as:\n\n- using `black` and `isort` without any arguments,\n- using the `editorconfig` configuration.\n\n### VScode\n\n- Recommend extensions to work well with c2cciutils:\n  - [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) And use EditorConfig\n  - [shell-format](https://marketplace.visualstudio.com/items?itemName=foxundermoon.shell-format) With the configuration\n    `"shellformat.flag": "-bn"`.\n  - [Better TOML](https://marketplace.visualstudio.com/items?itemName=bodil.prettier-toml)\n- Other recommend extensions:\n  - [hadolint](https://marketplace.visualstudio.com/items?itemName=exiasr.hadolint)\n  - [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)\n\nSelect a formatter:\n\n- `CTRL+MAJ+P`\n- Format document With...\n- Configure Default Formatter...\n- Select the formatter\n\n## Publishing\n\n### To pypi\n\nThe config is like this:\n\n```yaml\nversions:\n  # List of kinds of versions you want to publish, that can be:\n  # rebuild (specified with --type),\n  # version_tag, version_branch, feature_branch, feature_tag (for pull request)\n```\n\nIt we have a `setup.py` file, we will be in legacy mode:\nWhen publishing, the version computed from arguments or `GITHUB_REF` is put in environment variable `VERSION`, thus you should use it in `setup.py`, example:\n\n```python\nVERSION = os.environ.get("VERSION", "1.0.0")\n```\n\nAlso we consider that we use `poetry` with [poetry-dynamic-versioning](https://pypi.org/project/poetry-dynamic-versioning/) to manage the version, and [poetry-plugin-tweak-dependencies-version](https://pypi.org/project/poetry-plugin-tweak-dependencies-version/) to manage the dependencies versions.\n\nExample of configuration:\n\n```toml\n[tool.poetry-dynamic-versioning]\nenable = true\nvcs = "git"\npattern = "^(?P<base>\\\\d+(\\\\.\\\\d+)*)"\nformat-jinja = """\n{%- if env.get("VERSION_TYPE") == "version_branch" -%}\n{{serialize_pep440(bump_version(base, 1 if env.get("IS_MASTER") == "TRUE" else 2), dev=distance)}}\n{%- elif distance == 0 -%}\n{{serialize_pep440(base)}}\n{%- else -%}\n{{serialize_pep440(bump_version(base), dev=distance)}}\n{%- endif -%}\n"""\n\n```\n\nNote that we can access to the environment variables `VERSION`,`VERSION_TYPE` and `IS_MASTER`.\n\nThen by default:\n\n- Tag with `1.2.3` => release `1.2.3`\n- Commit on feature branch just do a validation\n- Commit on `master` branch after the tag 1.3.0 => release `1.4.0.dev1`\n- Commit on `1.3` branch after the tag 1.3.0 => release `1.3.1.dev1`\n\nTo make it working in the `Dockerfile` you should have in the `poetry` stage:\n\n```Dockerfile\nENV POETRY_DYNAMIC_VERSIONING_BYPASS=dev\nRUN poetry export --extras=checks --extras=publish --extras=audit --output=requirements.txt \\\n    && poetry export --with=dev --output=requirements-dev.txt\n```\n\nAnd in the `run` stage\n\n```Dockerfile\nARG VERSION=dev\nRUN --mount=type=cache,target=/root/.cache \\\n    POETRY_DYNAMIC_VERSIONING_BYPASS=${VERSION} python3 -m pip install --disable-pip-version-check --no-deps --editable=.\n```\n\nAnd in the `Makefile`:\n\n```Makefile\nVERSION = $(strip $(shell poetry version --short))\n\n.PHONY: build\nbuild: ## Build the Docker images\n    docker build --build-arg=VERSION=$(VERSION) --tag=$(GITHUB_REPOSITORY) .\n```\n\n### To Docker registry\n\nThe config is like this:\n\n```yaml\nlatest: True\nimages:\n  - # The base name of the image we want to publish\n    name:\nrepository:\n  <internal_name>:\n    # The fqdn name of the server if not Docker hub\n    server:\n    # List of kinds of versions you want to publish, that can be: rebuild (specified using --type),\n    # version_tag, version_branch, feature_branch, feature_tag (for pull request)\n    version:\n    # List of tags we want to publish interpreted with `template(version=version)`\n    # e.g. if you use `{version}-lite` when you publish the version `1.2.3` the source tag\n    # (that should be built by the application build) is `latest-lite`, and it will be published\n    # with the tag `1.2.3-lite`.\n    tags:\n    # If your images are published by different jobs you can separate them in different groups\n    # and publish them with `c2cciutils-publish --group=<group>`\n    group:\n```\n\nBy default, the last line of the `SECURITY.md` file will be published (`docker`) with the tag\n`latest`. Set `latest` to `False` to disable it.\n\nWith the `c2cciutils-clean` the images on Docker hub for `feature_branch` will be removed on branch removing.\n\n## Download applications\n\nIn case some executables or applications from GitHub releases or any other URLs are required on the CI host\nand are not handled by any dependency manager, we provide a set of tools to install them and manage upgrades\nthrough Renovate.\n\nCreate an application file (e.-g. `applications.yaml`) with:\n\n```yaml\n# yaml-language-server: $schema=https://raw.githubusercontent.com/camptocamp/c2cciutils/master/c2cciutils/schema-applications.json\n\n# Application from GitHub release\n<organization>/<project>:\n  get-file-name: <file name present in the release>\n  to-file-name: <The file name you want to create in ~/.local/bin>\n  finish-command: # The command you want to run after the file is downloaded\n    - - chmod # To be executable (usually required)\n      - +x\n      - <to-file-name>\n    - - <to-file-name> # Print the version of the application\n      - --version\n# Application from GitHub release in a tar file (or tar.gz)\n<organization>/<project>:\n  get-file-name: <file name present in the release>\n  type: tar\n  tar-file-name: <The file name available in the tar file>\n  to-file-name: <The file name you want to create in ~/.local/bin>\n  finish-command: [...] # The command you want to run after the file is downloaded\n# Application from an URL\n<application reference name>:\n  url-pattern: <The URL used to download the application>\n  to-file-name: <The file name you want to create in ~/.local/bin>\n  finish-command: [...] # The command you want to run after the file is downloaded\n```\n\nIn the attributes `url-pattern`, `get-file-name` you can use the following variables:\n\n- `{version}`: The version of the application present in the version file.\n- `{version_quote}`: The URL encoded version.\n- `{short_version}`: The version without the `v` prefix.\n\nThe `applications-versions.yaml` file is a map of applications and their versions.\n\nAdd in your Renovate configuration:\n\n```json5\n  regexManagers: [\n    {\n      fileMatch: [\'^applications-versions.yaml$\'],\n      matchStrings: [\n        \'(?<depName>[^\\\\s]+): (?<currentValue>[^\\\\s]+) # (?<datasource>[^\\\\s]+)\',\n      ],\n    },\n  ],\n```\n\nNow you need to call `c2cciutils-download-applications --applications-file=applications.yaml --versions-file=applications-version.yaml`\nto install required applications on CI host before using them (an already installed application is installed only if needed).\n\n## Use Renovate to trigger a new build instead of the legacy rebuild\n\nRun the command `c2cciutils-docker-versions-gen camptocamp/image[:tag]` to generate a file that is a kind of package lock of the Debian packages in the file `ci/dpkg-versions.yaml`.\n\nAdd in your renovate configuration:\n\n```javascript\n  regexManagers: [\n    {\n      fileMatch: [\'^ci/dpkg-versions.yaml$\'],\n      matchStrings: [" *(?<depName>[^\'\\\\s]+): \'?(?<currentValue>[^\'\\\\s/]*[0-9][^\'\\\\s/]*)\'?"],\n      datasourceTemplate: \'repology\',\n      versioningTemplate: \'loose\',\n    },\n  ],\n```\n\nWhen a new version of a Debian package will be available:\n\n- Renovate will automatically open a pull request to update the file `ci/dpkg-versions.yaml`.\n- And the continuous integration will build a new fresh Docker image with latest versions of all Debian packages.\n\n## Kubernetes\n\nC2cciutils provide some commands for Kubernetes.\n\nYou can define a workflow like that:\n\n```yaml\n- name: Install k3s/k3d (Kubernetes cluster)\n  run: c2cciutils-k8s-install\n\n- name: Create a database to do the tests\n  run: c2cciutils-k8s-db --script=<my_script>.sql\n\n- name: Install the application in the Kubernetes cluster\n  run: kubectl apply -f <my_application>.yaml\n\n- name: Wait that the application is ready\n  run: c2cciutils-k8s-wait\n- name: Print the application status and logs\n  run: c2cciutils-k8s-logs\n  if: always()\n\n- name: Uninstall the application\n  run: kubectl delete -f <my_application>.yaml || true\n\n- name: Cleanup the database\n  run: c2cciutils-k8s-db --cleanup\n```\n\n`c2cciutils-k8s-install` can be configured in the `ci/config.yaml` file, in section `k8s/k3d/install-commands`, default is:\n\n```yaml\n- - k3d\n    cluster\n    create\n    test-cluster\n    --no-lb\n    --no-rollback\n```\n\nSee also: [K3d cluster create documentation](https://k3d.io/v4.4.8/usage/commands/k3d_cluster_create/).\n\n`c2cciutils-k8s-db` can be configured in the `ci/config.yaml` file, in section `k8s/db/chart-options`, default is:\n\n```yaml\npersistence.enabled: \'false\'\ntls.enabled: \'true\'\ntls.autoGenerated: \'true\'\npostgresqlPassword: mySuperTestingPassword\nvolumePermissions.enabled: \'true\'\n```\n\nSee also: [Parameters documentations](https://github.com/bitnami/charts/tree/master/bitnami/postgresql#parameters).\n\n## Contributing\n\nInstall the pre-commit hooks:\n\n```bash\npip install pre-commit\npre-commit install --allow-missing-config\n```\n',
    'author': 'Camptocamp',
    'author_email': 'info@camptocamp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/camptocamp/c2cciutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
