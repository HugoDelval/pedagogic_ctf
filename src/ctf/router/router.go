package router

import(
	"github.com/gorilla/mux"
	"ctf/utils"
	"ctf/handlers"
	"ctf/model"
)

var routes = model.Routes{
	model.Route{
		"Index",
		"GET",
		"/",
		handlers.Index,
	},
	model.Route{
		"TodoIndex",
		"GET",
		"/todo",
		handlers.TodoIndex,
	},
	model.Route{
		"TodoShow",
		"GET",
		"/todo/{todoId}",
		handlers.TodoShow,
	},
	model.Route{
		"TodoCreate",
		"POST",
		"/todo",
		handlers.TodoCreate,
	},

}


func NewRouter() *mux.Router {

	router := mux.NewRouter().StrictSlash(true)
	for _, route := range routes {
		handler := utils.Logger(route.HandlerFunc, route.Name)

		router.
		Methods(route.Method).
			Path(route.Pattern).
			Name(route.Name).
			Handler(handler)
	}

	return router
}