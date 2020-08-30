import sys,pprint,subprocess,pkg_resources

if ((len(sys.argv) -1) != 1 ):
    print("Error in args. Please run --> python {0} ./installed.txt".format(sys.argv[0]))
    sys.exit()

print("Let's find out what is required...............")
file1 = open(sys.argv[1],'r')
lines = file1.readlines();
requiredPkgDict = {}
requiredPkgSet = set()
for line in lines:
    (key,val) = line.split('==')
    requiredPkgDict.update({key:val})
    requiredPkgSet.add(key)
pprint.pprint("The required Packages are:")
pprint.pprint(requiredPkgSet)


print("Let's find out what is installed...............")
installedPkgSet = {pkg.key for pkg in pkg_resources.working_set}
pprint.pprint("The installed Packages are:")
pprint.pprint(installedPkgSet)

missingPkgSet = requiredPkgSet - installedPkgSet

if missingPkgSet :
    pprint.pprint("The misssing Packages are:")
    pprint.pprint(missingPkgSet)
    pprint.pprint("Installing them...")
    python = sys.executable
    subprocess.check_all([python, '-m', 'pip', 'install', *missingPkgSet],stdout=subprocess.DEVNULL)
else:
    pprint.pprint("No PKgs are missed, you are all set")
    
print("Completed Successfully")
