/*
 * FBModal 1.0.0 - jQuery Plugin
 *
 * @example $(".YOURDIV").fbmodal({options}); 
 * 
 * FBModal default options
 *
 *        title: "YOUR TITLE HERE",   Dialog title text 
 *       cancel: "Cancel",            Cancel button text
 *         okay: "Okay",              Okay button text
 *   okaybutton: true,                show the ok button
 * cancelbutton: true,                Show the cancel button
 *      buttons: true,                Show the buttons
 *      opacity: 0.0,                 The opacity value for the overlay div, from 0.0 - 100.0
 *	    fadeout: true,                When dialog is closed fade out
 * overlayclose: true,                Allow click on overlay to close the dialog?
 *     modaltop: "30%",               Position from top of page 0% - 100% or 0px - 99999px
 *   modalwidth: "400"                The width for the dialog container 
 * });
 *
 * SFBModal has been tested in the following browsers:
 * - IE 8
 * - Firefox 2, 3
 * - Safari 3, 4
 * - Chrome 1, 2
 *
 * @name FBModal
 * @type jQuery
 * @requires jQuery v1.4.2
 * @cat Plugins/Windows and Overlays
 * @author Barrett Palmer (http://www.sucaijiayuan.com)
 * @version 1.0.0
 *
 */
(function($){
$.fn.fbmodal = function(options, callback){  
  var defaults = {  
        title: "详情信息",  
       cancel: "取消",
         okay: "确定",
   okaybutton: true,
 cancelbutton: true,
      buttons: true,
      opacity: 0.0,
	  fadeout: true,
 overlayclose: true,
     modaltop: "30%",
   modalwidth: ""
  };
var options = $.extend(defaults, options);
var fbmodalHtml='\
<div id="fbmodal" > \
<div class="popup"> \
<table> \
<tbody> \
<tr> \
<td class="tl"/><td class="b"/><td class="tr"/> \
</tr> \
<tr> \
<td class="b"/> \
<td class="body"> \
<div class="title">\
</div> \
<div class="container">\
<div class="content">\
</div> \
<div class="footer"> \
<div class="right">\
<div class="button_outside_border_blue" id="ok">\
<div class="button_inside_border_blue" id="okay">\
</div>\
</div>\
<div class="button_outside_border_grey" id="close">\
<div class="button_inside_border_grey" id="cancel">\
</div>\
</div>\
</div>\
<div class="clear">\
</div>\
</div> \
</div>\
</td> \
<td class="b"/>\
</tr> \
<tr> \
<td class="bl"/><td class="b"/><td class="br"/> \
</tr> \
</tbody> \
</table> \
</div> \
</div>';
var preload = [ new Image(), new Image() ]
$("#fbmodal").find('.b:first, .bl, .br, .tl, .tr').each(function() {
  preload.push(new Image())
  preload.slice(-1).src = $(this).css('background-image').replace(/url\((.+)\)/, '$1')
})	
var dat=this.html();
$("body").append(fbmodalHtml);
$("#fbmodal .content").append('<div class="loading"><img src="images/loading.gif"/></div>');
$("#fbmodal").css("top",options.modaltop);
if(options.okaybutton == false || options.buttons == false){
$("#fbmodal #ok").hide();
}
if(options.cancelbutton == false || options.buttons == false){
$("#fbmodal #close").hide();
}
$("#fbmodal .title").append(options.title);
$("#fbmodal #okay").append(options.okay);
$("#fbmodal #cancel").append(options.cancel);
$("#fbmodal .content").append(dat).css("width",options.modalwidth);
$("#fbmodal .loading").remove();
$("body").append('<div id="fbmodal_overlay" class="fbmodal_hide"></div>');
$("#fbmodal_overlay").addClass("fbmodal_overlay").fadeTo(0,options.opacity);
fbWidth();
$(window).bind("resize", function(){  
fbWidth();  
}); 
function fbWidth(){ 
var windowWidth=$(window).width();
var fbmodalWidth=$("#fbmodal").width();
var fbWidth=windowWidth / 2 - fbmodalWidth / 2;
$("#fbmodal").css("left",fbWidth);
}
if(options.close == true){ 
if(options.fadeout == true){
$("#fbmodal").fadeOut( function(){
$("#fbmodal").remove();
$("#fbmodal_overlay").removeClass("fbmodal_overlay");
});
}else{
$("#fbmodal").remove();
$("#fbmodal_overlay").removeClass("fbmodal_overlay");
}
}
if(options.overlayclose == true){
var overlay="ok, #close, .fbmodal_hide"
}else{
var overlay="ok, #close"
}
$("#"+overlay).click( function(){
if(options.fadeout == true){
$("#fbmodal").fadeOut( function(){
$("#fbmodal").remove();
$("#fbmodal_overlay").removeClass("fbmodal_overlay");
});
}else{
$("#fbmodal").remove();
$("#fbmodal_overlay").removeClass("fbmodal_overlay");
}
});
$("#fbmodal #okay").click(function() {
var okay=1;
callback(okay);
});
$("#fbmodal #cancel").click(function() {
var cancel=2;
callback(cancel);
});
}
})(jQuery); 