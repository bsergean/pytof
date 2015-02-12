#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

void sha(char *string, char outputBuffer[65])
{
    unsigned char hash[SHA_DIGEST_LENGTH];
    SHA_CTX sha;
    SHA1_Init(&sha);
    SHA1_Update(&sha, string, strlen(string));
    SHA1_Final(hash, &sha);
    int i = 0;
    for(i = 0; i < SHA_DIGEST_LENGTH; i++)
    {
        sprintf(outputBuffer + (i * 2), "%02x", hash[i]);
    }
    outputBuffer[64] = 0;
}

int main()
{
    static unsigned char buffer[65];
    sha256("string", buffer);
    printf("%s\n", buffer);
}
