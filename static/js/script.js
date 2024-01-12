function parallax_height() {
    var scroll_top = $(this).scrollTop();
    var sample_section_top = $(".sample-section").offset().top;
    var header_height = $(".sample-header-section").outerHeight();
    $(".sample-section").css({ "margin-top": header_height + 100 });
    $(".sample-header").css({ height: header_height + 100 - scroll_top });
}
parallax_height();
$(window).scroll(function () {
    parallax_height();
});
$(window).resize(function () {
    parallax_height();
});

$(document).ready(function () {
    $("#act").on("change", function () {
        console.log("changing");
        console.log(this.value);
        for (i = 1; i <= 7; i++) {
            $(`#act${i}`).hide();
        }
        $(`#${this.value}`).show();
    });
});
