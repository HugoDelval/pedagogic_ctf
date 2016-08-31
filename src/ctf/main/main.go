package main

import (
	"log"
	"net/http"
	"ctf/router"
	"ctf/model"
)

func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
	router := router.NewRouter()

	model.Migrate()

	log.Fatal(http.ListenAndServe("127.0.0.1:8080", router))
}
