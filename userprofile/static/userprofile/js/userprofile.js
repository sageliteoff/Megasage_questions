
Time  = function () {

  this.convertMillisecondsToDays = function (milliseconds) {
    //convertMillsecondsToDays
    // 1 day == 86400000 milliseconds
    days = Math.floor(milliseconds / 86400000)
    return days
  }

  this.convertMillsecondsToHours = function (milliseconds) {
    // 1 hour == 3600000 milliseconds
    hours = Math.floor(milliseconds / 3600000)
    return hours
  }

  this.convertMillsecondsToMinutes = function (milliseconds) {
    // 1 minutes == 60000 milliseconds
    minutes = Math.floor(milliseconds / 60000)
    return minutes
  }

  this.convertMillsecondsToSeconds = function (milliseconds) {
    // 1 second == 1000 milliseconds
    seconds = Math.floor(milliseconds / 1000)
    return seconds
  }

  this.countDown = function (date) {
    if(date){
      d = new Date(date)
      if (d == "Invalid Date"){
          return `Invalid Date format. <year-month-day hour:minute:second> eg: "2018-1-25 8:20:0"`
        }
      totalmilliseconds = d - $.now()
      if (totalmilliseconds < 0){
          return  `Time up ${this.convertMillsecondsToSeconds(totalmilliseconds)} seconds`
      }
      millisecondsAfterDays = totalmilliseconds % 86400000
      millisecondsAfterHours = totalmilliseconds % 3600000
      millisecondsAfterMinute = totalmilliseconds % 60000
      return `${this.convertMillisecondsToDays(totalmilliseconds)} days ${this.convertMillsecondsToHours(millisecondsAfterDays)}: ${this.convertMillsecondsToMinutes(millisecondsAfterHours)}: ${this.convertMillsecondsToSeconds(millisecondsAfterMinute)}`
    }
    return "provide date as string in this formart <year-month-day hour:minute:second>"
  }

  this.now = function () {
    return new Date($.now())
  }
}

$(this).ready(function () {

  //create a string in the format year-months-day hours:minutes:seconds
  date = `${$("#year").text()}-${$("#month").text()}-${$("#day").text()} ${$("#hour").text()}:${$("#minute").text()}:${$("#second").text()}`

  //remove the container of date_parameters from the documents because it has no use again
  $("#date_parameters_container").remove();

  setInterval(function () {
    time = new Time() // create a new time object
    $("#days_left").text(time.countDown(date)); //update the text of the date_left element
  },500)

})
