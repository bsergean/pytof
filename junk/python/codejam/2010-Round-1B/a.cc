#include <iostream>
#include <vector>
#include <set>
#include <string>

class FS
{
public:
    FS() {}

    int mkdir(const std::string& path);
    std::string dirname(const std::string& path);

private:
    bool isRoot(const std::string& path);
    std::string root() { return "/"; }

    typedef std::set<std::string> Folders;
    Folders mFolders;
};

bool
FS::isRoot(const std::string& path)
{
    return path == "/";
}

int
FS::mkdir(const std::string& path)
{
    Folders::const_iterator it;
    it = mFolders.find(path);
    if (it != mFolders.end()) {
        return 0;
    }

    if (isRoot(path)) {
        return 0;
    }

    std::string dn = dirname(path);
    mFolders.insert(path);

    return 1 + mkdir(dn);
}

std::string
FS::dirname(const std::string& path)
{
    if (isRoot(path)) {
        return std::string("");
    }

    unsigned found = path.find_last_of("/");
    if (found == 0) {
        return root();
    }

    return path.substr(0, found); 
}

int
main()
{
    if (false) {
        FS fs;
        std::cout << fs.dirname("/home/bsergean") << std::endl;
        std::cout << fs.dirname("/home") << std::endl;
        std::cout << fs.dirname("/") << std::endl;
        std::cout << fs.dirname("") << std::endl;
        std::cout << fs.dirname("home") << std::endl;

        std::cout << "MKDIR" << std::endl;
        std::cout << fs.mkdir("/home/bsergean") << std::endl;
        std::cout << fs.mkdir("/home") << std::endl;
        std::cout << fs.mkdir("/usr/lib/exec") << std::endl;
    }

    int T;
    std::cin >> T;
    
    for (int d = 0; d < T; ++d) {
        int N;
        std::cin >> N;
        int M;
        std::cin >> M;

        FS fs;

        for (int j = 0; j < N; ++j) {
            std::string temp;
            std::cin >> temp;
            fs.mkdir(temp);
        }

        int created = 0;
        for (int j = 0; j < M; ++j) {
            std::string temp;
            std::cin >> temp;
            created += fs.mkdir(temp);
        }

        std::cout << "Case #" << d+1 << ": "
                  << created << std::endl;
    }
}
