package main

import (
    "fmt"
    "os"
    "regexp"
    "os/exec"
)

func main() {
    // check params
    args := os.Args[1:]
    if len(args) != 1 || args[0] == "" {
        fmt.Println("Please send me a server address so I can dig it ! (ex: 127.0.0.1 or www.ovh.com)")
        os.Exit(0)
    }
    server := args[0]
    regexServerCompiled := regexp.MustCompile("[!;&|'\"`${}><]")
    if regexServerCompiled.MatchString(server){
        fmt.Println("Error, server param not valid.")
        os.Exit(0)
    }
    // end check params

    // launch dig
    command := "/usr/bin/dig " + server 
    resultDig, _ := exec.Command("sh", "-c", command).CombinedOutput()
    // end launch dig

    fmt.Println(string(resultDig[:]))
}
