package router

import (
	"ctf/handlers"
	"ctf/model"
	"ctf/utils"
	"github.com/gorilla/mux"
	"net/http"
)

var routes = model.Routes{
	model.Route{
		"Index",
		"GET",
		"/v1.0",
		handlers.Index,
	},
	model.Route{
		"Scoreboard",
		"GET",
		"/v1.0/scoreboard",
		handlers.GetScoreboard,
	},
	model.Route{
		"ChallengeShowAll",
		"GET",
		"/v1.0/challenge",
		handlers.ChallengeShowAll,
	},
	model.Route{
		"ChallengeShow",
		"GET",
		"/v1.0/challenge/{challengeName}",
		handlers.ChallengeShow,
	},
	model.Route{
		"ChallengeValidate",
		"POST",
		"/v1.0/challenge/{challengeName}/validate",
		handlers.ChallengeValidate,
	},
	model.Route{
		"ChallengeExecute",
		"POST",
		"/v1.0/challenge/{challengeName}/execute",
		handlers.ChallengeExecute,
	},
	model.Route{
		"ChallengeCorrect",
		"POST",
		"/v1.0/challenge/{challengeName}/correct",
		handlers.ChallengeCorrect,
	},
	model.Route{
		"UserAuthenticate",
		"POST",
		"/v1.0/user/login",
		handlers.UserAuthenticate,
	},
	model.Route{
		"UserRegister",
		"POST",
		"/v1.0/user/register",
		handlers.UserRegister,
	},
	model.Route{
		"UserShowOwn",
		"GET",
		"/v1.0/user/me",
		handlers.UserShowOwn,
	},
	model.Route{
		"UserShow",
		"GET",
		"/v1.0/user/{userID}",
		handlers.UserShow,
	},
	model.Route{
		"UserShowAll",
		"GET",
		"/v1.0/user",
		handlers.UserShowAll,
	},
	model.Route{
		"UserShowValidatedChallenges",
		"GET",
		"/v1.0/user/{userID}/validatedChallenges",
		handlers.UserShowValidatedChallenges,
	},
	model.Route{
		"UserChangePassword",
		"PUT",
		"/v1.0/user/me/changePassword",
		handlers.UserChangePassword,
	},
	model.Route{
		"UserDelete",
		"DELETE",
		"/v1.0/user/me/unregister",
		handlers.UserDelete,
	},
	model.Route{
		"UserLogout",
		"POST",
		"/v1.0/user/logout",
		handlers.UserLogout,
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
	if !utils.GetConfig().IsProduction {
		router.PathPrefix("/").Handler(http.FileServer(http.Dir("/srv/ctf_go/frontend-angular/app/")))
		http.Handle("/", router)
	}

	return router
}
