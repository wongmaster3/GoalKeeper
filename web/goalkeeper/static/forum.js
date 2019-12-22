var toolbarOptions = [
    [{ 'header': [1, 2, 3, false] }],
    ['bold', 'italic', 'underline', 'strike', { 'script': 'sub'}, { 'script': 'super' }],
    ['link', 'blockquote', 'code-block', 'image'],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'indent': '-1'}, { 'indent': '+1' }],
    [{ 'align': [] }],
    ['clean']
];

var quill;

document.addEventListener('DOMContentLoaded', function() {
    quill = new Quill('#editor', {
        modules: {
            toolbar: toolbarOptions
        },
        placeholder: "Type here",
        theme: 'snow'
    });

    var form = document.querySelector('form');
    form.onsubmit = function() {
        var post = document.querySelector('input[name=post]');
        if(quill.getText().trim().length > 0) {
            post.value = quill.root.innerHTML;
        }else{
            post.value = "";
        }
    };
}, false);

function set_reply(id) {
    var reply_to = document.querySelector('input[name=replyto]');
    reply_to.value = id;
}

function reset_editor() {
    if(quill.getText().trim().length > 0) {
        var conf = confirm("Discard post draft?")
        if (conf == true) {
            quill.setText('');
        }
    } else {
        quill.setText('');
    }
}