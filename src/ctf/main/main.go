package main

import (
	"ctf/handlers"
	"ctf/router"
	"ctf/utils"
	"log"
	"net/http"
)

func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
	router := router.NewRouter()

	handlers.InitDB("sqlite3", "database.db")
	handlers.Migrate()

	if utils.GetConfig().IsProduction {
		log.Fatal(http.ListenAndServe("127.0.0.1:8080", router))
	} else {
		log.Fatal(http.ListenAndServe("0.0.0.0:8080", router))
	}
}
