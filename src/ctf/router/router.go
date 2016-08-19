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
		"ChallengeShowAll",
		"GET",
		"/challenge",
		handlers.ChallengeShowAll,
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
	model.Route{
		"UserAuthenticate",
		"POST",
		"/user/login",
		handlers.UserAuthenticate,
	},
	model.Route{
		"UserRegister",
		"POST",
		"/user/register",
		handlers.UserRegister,
	},
	model.Route{
		"UserRegister",
		"POST",
		"/user/register",
		handlers.UserRegister,
	},
	model.Route{
		"UserShowOwn",
		"GET",
		"/user/me",
		handlers.UserShowOwn,
	},
	model.Route{
		"UserShow",
		"GET",
		"/user/{userID}",
		handlers.UserShow,
	},
	model.Route{
		"UserShowAll",
		"GET",
		"/user",
		handlers.UserShowAll,
	},
	model.Route{
		"UserShowValidatedChallenges",
		"GET",
		"/user/{userID}/validatedChallenges",
		handlers.UserShowValidatedChallenges,
	},
	model.Route{
		"UserChangePassword",
		"PUT",
		"/user/me/changePassword",
		handlers.UserChangePassword,
	},
	model.Route{
		"UserDelete",
		"DELETE",
		"/user/me/unregister",
		handlers.UserDelete,
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