package handlers

import (
	"net/http"
	"ctf/model"
	"github.com/gorilla/mux"
	"ctf/utils"
	"log"
	"encoding/json"
)

func TodoIndex(w http.ResponseWriter, r *http.Request) {
	todos := model.Todos{
		model.Todo{Name: "Write presentation"},
		model.Todo{Name: "Host meetup"},
	}

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, todos)
}

func TodoShow(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	todoId := vars["todoId"]
	utils.SendResponseJSON(w, todoId)
}

func TodoCreate(w http.ResponseWriter, r *http.Request) {
	var todoRaw []byte
	var todo model.Todo
	if err := utils.LoadJSONFromRequest(w, r, &todoRaw); err != nil{
		return
	}
	if err := json.Unmarshal(todoRaw, &todo); err != nil{
		utils.SendResponseJSON(w, utils.Message{Message: "Bad request"})
		log.Println(err)
		return
	}

	w.WriteHeader(http.StatusCreated)
	utils.SendResponseJSON(w, todo)
}
