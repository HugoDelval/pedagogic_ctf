package main

import (
    "fmt"
    "os"
    "regexp"
    "os/exec"
)

// Usage :
// go run ./command_injection.go <server_address>
// ex: go run ./command_injection.go www.ovh.com
// do a dig on this server

func main() {
    // check params
    args := os.Args[1:]
    if len(args) != 1 || args[0] == "" {
        fmt.Println("Please send me a server address so I can dig it ! (ex: google.com or www.ovh.com)")
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
    command := "/usr/bin/dig +short " + server
    resultDig, _ := exec.Command("sh", "-c", command).CombinedOutput()
    // end launch dig

    fmt.Println(string(resultDig[:]))
}
