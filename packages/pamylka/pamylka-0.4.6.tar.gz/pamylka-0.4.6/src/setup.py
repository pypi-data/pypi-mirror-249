from pam import AlphaApp, find


pam = AlphaApp(
        "pam",
        "00.04.06",
        "Programming",
        "13/3/1445 Higri",
        app="python module",
        execute=False,
        root="src"
    )
with open(find("pyproject.toml", "../")) as file:
    toml = file.readlines()

for i in range(len(toml)):
    if "version" in toml[i]:
        toml[i] = f'version = "{pam.version}"\n'

with open(find("pyproject.toml", "../"), "w") as file:
    file.writelines(toml)

print(pam)