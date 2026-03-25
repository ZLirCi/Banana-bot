function doGet(e) {
  return handleRequest(e);
}

function doPost(e) {
  return handleRequest(e);
}

function handleRequest(e) {
  var data = {};
  try {
    if (e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    }
  } catch (err) {}

  var action = (e.parameter && e.parameter.action) || data.action;
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var lastRow = sheet.getLastRow();

  function formatDateValue(val) {
    if (!val && val !== 0) return "";
    if (Object.prototype.toString.call(val) === "[object Date]") {
      var d = val;
      return ("0" + d.getDate()).slice(-2) + "." +
             ("0" + (d.getMonth() + 1)).slice(-2) + "." +
             d.getFullYear();
    }
    var s = String(val).trim();
    var re = /^(\d{1,2})[.\-\/](\d{1,2})[.\-\/](\d{2,4})$/;
    var m = s.match(re);
    if (m) {
      var dd = ("0" + m[1]).slice(-2);
      var mm = ("0" + m[2]).slice(-2);
      var yyyy = m[3].length == 2 ? ("20" + m[3]) : m[3];
      return dd + "." + mm + "." + yyyy;
    }
    return s;
  }

  // === ADD ===
  if (action == "add") {
    var date = e.parameter.date || data.date;
    var nick = e.parameter.nick || data.nick;
    var amount = e.parameter.amount || data.amount;
    sheet.appendRow([date, nick, amount]);
    return ContentService.createTextOutput("Added");
  }

  // balance
  if (action == "balance") {
    var nick = e.parameter.nick || data.nick;
    var total = 0;
    if (lastRow > 0) {
      var range = sheet.getRange(1, 1, lastRow, 3).getValues();
      for (var i = 0; i < range.length; i++) {
        if (range[i][1] == nick) total += Number(range[i][2]);
      }
    }
    return ContentService.createTextOutput("BALANCE:" + total);
  }

  // remove
  if (action == "remove") {
    var dateRaw = e.parameter.date || data.date;
    var nickRaw = e.parameter.nick || data.nick;
    if (!dateRaw || !nickRaw) return ContentService.createTextOutput("ERROR: missing date or nick");

    var targetDate = formatDateValue(dateRaw);
    var targetNick = String(nickRaw).trim();

    if (lastRow == 0) return ContentService.createTextOutput("NOT_FOUND");

    var range = sheet.getRange(1, 1, lastRow, 3).getValues();
    for (var i = 0; i < range.length; i++) {
      var cellDate = formatDateValue(range[i][0]);
      var cellNick = String(range[i][1]).trim();
      if (cellDate == targetDate && cellNick == targetNick) {
        sheet.deleteRow(i + 1);
        return ContentService.createTextOutput("SUCCESS");
      }
    }
    return ContentService.createTextOutput("NOT_FOUND");
  }

  // removeall
  if (action == "removeall") {
    var nickRaw = e.parameter.nick || data.nick;
    if (!nickRaw) return ContentService.createTextOutput("ERROR: missing nick");
    var targetNick = String(nickRaw).trim();
    if (lastRow == 0) return ContentService.createTextOutput("NOT_FOUND");

    var range = sheet.getRange(1, 1, lastRow, 3).getValues();
    var rowsToDelete = [];
    for (var i = 0; i < range.length; i++) {
      var cellNick = String(range[i][1]).trim();
      if (cellNick == targetNick) rowsToDelete.push(i + 1);
    }
    if (rowsToDelete.length == 0) return ContentService.createTextOutput("NOT_FOUND");
    for (var j = rowsToDelete.length - 1; j >= 0; j--) sheet.deleteRow(rowsToDelete[j]);
    return ContentService.createTextOutput("SUCCESS:" + rowsToDelete.length);
  }

  // history
  if (action == "history") {
    var nickRaw = e.parameter.nick || data.nick;
    if (!nickRaw) return ContentService.createTextOutput("ERROR: missing nick");
    var targetNick = String(nickRaw).trim();
    if (lastRow == 0) return ContentService.createTextOutput("NOT_FOUND");

    var range = sheet.getRange(1, 1, lastRow, 3).getValues();
    var result = [];
    for (var i = 0; i < range.length; i++) {
      var cellNick = String(range[i][1]).trim();
      if (cellNick == targetNick) {
        var cellDate = formatDateValue(range[i][0]);
        var amount = String(range[i][2]).trim();
        result.push(cellDate + " — " + amount);
      }
    }
    if (result.length == 0) return ContentService.createTextOutput("NOT_FOUND");
    return ContentService.createTextOutput(result.join("\n"));
  }

  return ContentService.createTextOutput("ERROR: unknown action");
}
