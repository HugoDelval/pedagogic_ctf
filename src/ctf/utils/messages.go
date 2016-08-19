package utils

var InternalErrorMessage = Message{Message: "Internal Servor Error, please contact an admin " + GetConfig().Emails}
var BadRequestMessage = Message{Message: "Bad request"}
var NotFoundErrorMessage = Message{Message: "The ressource you're looking for does not exists on the server."}
var NotLoggedInMessage = Message{Message: "You need to be logged in to do that."}