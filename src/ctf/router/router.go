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
		"ChallengeShow",
		"GET",
		"/challenge/{challengeName}",
		handlers.ChallengeShow,
	},
	model.Route{
		"ChallengeValidate",
		"POST",
		"/challenge/{challengeName}/validate",
		handlers.ChallengeValidate,
	},
	model.Route{
		"ChallengeExecute",
		"POST",
		"/challenge/{challengeName}/execute",
		handlers.ChallengeExecute,
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