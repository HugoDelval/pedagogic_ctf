package main

import (
    "fmt"
    "os"
    "regexp"
    "math/rand"
    "time"
    "os/exec"
)

// Usage :
// go run ./injection_conf.go <directory_path>
// ex: go run ./injection_conf.go /tmp/test
// create a config file (configurationFileName) containing a variable which value is set to <directory_path>
// then create a project based on this configuration file

func exists(path string) (bool) {
    _, err := os.Stat(path)
    if err == nil { return true }
    return false
}

func init() {
    rand.Seed(time.Now().UnixNano())
}

func randString(n int) string {
    var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    b := make([]rune, n)
    for i := range b {
        b[i] = letterRunes[rand.Intn(len(letterRunes))]
    }
    return string(b)
}

func main() {
    // check params
    args := os.Args[1:]
    if len(args) != 1 || args[0] == "" {
        fmt.Println("Please send me a directory path so I can launch my configuration script !")
        os.Exit(0)
    }
    directory := args[0]
    regexDirectoryCompiled := regexp.MustCompile(`(/tmp/|/srv/writable/)[a-zA-Z0-9_-]+`)
    if !regexDirectoryCompiled.MatchString(directory){
        fmt.Println("Error, directory param not valid.")
        os.Exit(0)
    }
    if exists(directory){
        fmt.Println("Directory already exists.")
        os.Exit(0)
    }
    // end check params

    // write configuration file
    configurationFileName := "/srv/writable/"
    configurationFileName += randString(30)
    configurationFileName += "_config.sh"
    f, _ := os.Create(configurationFileName)
    defer f.Close()
    _, _ = f.WriteString("DATE=`date`\n")
    _, _ = f.WriteString("DIRECTORY=" + directory + "\n")
    f.Sync()
    // end write configuration file

    // create project based on the config file
    command := ". " + configurationFileName + " && "
    command += "mkdir \"${DIRECTORY}\" && "
    command += "echo ${DATE} > \"${DIRECTORY}/folder_configured\""
    _, _ = exec.Command("sh", "-c", command).Output()
    // create project application based on the config file

    if exists(directory){
        fmt.Println("Directory configured.")
    }else{
        fmt.Println("Failed to configure directory.")
    }
}
