var currentMonth = new Date().getMonth();
var currentYear = new Date().getFullYear();
const monthNames = ["January", "February", "March", "April", "May", "June",
"July", "August", "September", "October", "November", "December"];

function incrementMonth(){
    currentMonth++;
    if(currentMonth > 11){
        currentMonth = 0;
        currentYear++;
    }
    setCalendar();
}

function decrementMonth(){
    currentMonth--;
    if(currentMonth < 0){
        currentMonth = 11;
        currentYear--;
    }
    setCalendar();
}

function clearNode(node){
    var child = node.lastElementChild;
    while(child){
        node.removeChild(child);
        child = node.lastElementChild;
    }
}

function on(day) {
    overlay = document.getElementById("overlay");
    overlay.style.display = "block";
    document.getElementById("goal_date").textContent = new Date(parseInt(day)).toDateString(); //new Date(long(day)).toString();
    document.getElementById("due_date").value = day;
}

function off() {
    document.getElementById("overlay").style.display = "none";
}

function color(title, date, description) {
    timestamp = parseFloat(date) * 1000;
    li = document.getElementById(timestamp);
    span = document.createElement("span");
    span.class = "highlight";
    span.id = "highlight";
}

function setCalendar(){
    var prevLastDay = new Date(currentYear, currentMonth, 0);
    var firstDay = new Date(currentYear, currentMonth, 1);
    var lastDay = new Date(currentYear, currentMonth + 1, 0);
    var dayBuffer = firstDay.getDay();
    var ul = document.getElementById("days");
    clearNode(ul);
    for(i = 0; i < dayBuffer; i++){
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(prevLastDay.getDate() + 1 - (dayBuffer - i)));
        li.id= new Date(currentYear, currentMonth-1, prevLastDay.getDate() + 1 - (dayBuffer - i)).getTime();
        li.onclick = (function(x) { return function() { on(x); }; })(li.id);
        ul.appendChild(li);
    }
    for(i = 0; i < lastDay.getDate(); i++){
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(i + 1));
        li.id= new Date(currentYear, currentMonth, i + 1).getTime();
        li.onclick = (function(x) { return function() { on(x); }; })(li.id);
        ul.appendChild(li);
    }

    var monthText = document.getElementById("monthText");
    monthText.textContent = monthNames[currentMonth];
    var yearText = document.getElementById("yearText");
    yearText.textContent = currentYear;
}