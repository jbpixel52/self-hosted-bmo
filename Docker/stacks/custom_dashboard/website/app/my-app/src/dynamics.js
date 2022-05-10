
function greeting() {
  const generic_greetings = [
      "Good Morning",
      "Wassup",
      "Hello",
      "What u doing?..",
      "Ayooo!",
    ];
  let greetingIndex = Math.floor(Math.random() * generic_greetings.length);
  return (<h1>{generic_greetings[greetingIndex]}, you!</h1>)
}

export {greeting, getTime}

function getTime() {
  var today = new Date();   
  let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  return(<h1>{time}</h1>)
}