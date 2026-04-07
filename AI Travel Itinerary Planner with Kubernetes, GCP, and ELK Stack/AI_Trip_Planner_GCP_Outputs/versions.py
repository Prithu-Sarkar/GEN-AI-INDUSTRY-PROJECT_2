from importlib.metadata import version, PackageNotFoundError

PACKAGES = [
    'langchain', 'langchain-core', 'langchain-community',
    'langchain-groq', 'langchain-tavily',
    'langchain-text-splitters', 'python-dotenv',
]

def get_package_version(pkg_name):
    try:
        return version(pkg_name)
    except PackageNotFoundError:
        return 'NOT INSTALLED'

def print_versions():
    versions = {pkg: get_package_version(pkg) for pkg in PACKAGES}
    return versions

if __name__ == '__main__':
    v = print_versions()
    print('\n📦 Installed Package Versions:\n')
    for k, val in v.items():
        print(f'  {k:35} == {val}')
    print('')
