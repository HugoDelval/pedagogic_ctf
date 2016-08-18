package utils

import (
	"os"
	"encoding/json"
	"log"
)

type Configuration struct {
	Emails       string
	IsProduction bool
}

func GetConfig() *Configuration {
	file, err := os.Open("/srv/ctf_interne/src/ctf/utils/config.json")
	if err != nil{
		log.Println(err)
	}
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	if err = decoder.Decode(&configuration); err != nil {
		log.Println(err)
	}
	return &configuration
}
