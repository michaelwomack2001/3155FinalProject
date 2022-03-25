function deleteNote(noteId) {
    fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
    window.location.href = "/trade";
    });
}

function deleteTrade(tradeId) {
    fetch("/delete-trade", {
    method: "POST",
    body: JSON.stringify({ tradeId: tradeId }),
    }).then((_res) => {
    window.location.href = "/trade";
    });
}