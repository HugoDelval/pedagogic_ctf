package main

import (
	"log"
	"net/http"
	"ctf/router"
	"ctf/utils"
	"ctf/model"
)

func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
	router := router.NewRouter()

	model.Migrate()
	if utils.GetConfig().IsProduction{
		log.Fatal(http.ListenAndServe("127.0.0.1:8080", router))
	}else{
		log.Fatal(http.ListenAndServe("0.0.0.0:8080", router))
	}
}
