$(document).ready(function() {
    renderHome();
    $('.arrow-down').addClass('animated bounce');
    
    var topH = $('.navbar-wrapper').first().height();
    var maxH = $(window).height() - topH - 50;
    $('.relatednews').height(maxH);
    $(".relatednews").niceScroll();
    
    //balance height
    if ($(window).width() > 600)
    {
        balanceHeight('.latestnews .col-lg-3');
        balanceHeight('.about .item');
        balanceHeight('.stastitic .item');
    }
    
    //slider homepage
    var maxWidth = $('#bottomCarousel').width()/2 + 100;
    if ($('#bottomCarousel').length > 0)
        var homeSlider = $('#bottomCarousel .carousel-inner').bxSlider({
            infiniteLoop:false,
            moveSlides:1, 
            maxSlides:2, 
            controls:true, 
            pager: true, 
            slideWidth: maxWidth,
            onSlideBefore: function (slideElement, oldIndex, newIndex) {
                lastSlide(homeSlider);
            }
        });
    
    //company management
    startSlider();
    initCareers();
    renderCompany();
});

$(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

$(function() {
  var eTop = $(window).scrollTop();
  
  $(window).scroll(function() {
      if( (eTop >= $(window).scrollTop()) && $(window).scrollTop() > 0)
          $('#affixNav').addClass('affix');
      else
          $('#affixNav').removeClass('affix');
      eTop = $(window).scrollTop();
      
      //renderCompany();
  });
  
  $('body').on({
      'touchmove': function(e) { 
          if( (eTop >= $(window).scrollTop()) && $(window).scrollTop() > 0)
              $('#affixNav').addClass('affix');
          else
              $('#affixNav').removeClass('affix');
          eTop = $(window).scrollTop();
      
          //renderCompany();
      }
  });
});

$(window).resize(function() {
    renderHome();
    renderCompany();
});

function initCareers()
{
    $(".zinio-opening-list .rbox-opening-li > a").on('click', function(e){
        e.preventDefault();
        
        var id = $(this).attr('href');
        $('.zinio-opening-list .zinio-opening-detail').html($(id).html()).show();
        $(".rbox-opening-list").hide();
        $(".job-opening-list").hide();
        
        $(".zinio-opening-list a[href='#openings-list']").on('click', function(e){
            e.preventDefault();
            $('.zinio-opening-list .zinio-opening-detail').html('').hide();
            $('.zinio-opening-list .zinio-opening-detail .rbox-application').html('');
            $(".rbox-opening-list").show();
            $(".job-opening-list").show();
        });
        
        $(".zinio-opening-list .rbox-apply-button").on('click', function(e){
            e.preventDefault();
            $('.zinio-opening-list .zinio-opening-detail .rbox-application').html($('.zinio-opening-list .form-application').html());
            $('.zinio-opening-list .zinio-opening-detail .rbox-application').find('input[name="subject"]').attr('value', $(this).attr('data-subject'));
        });
    });
}

function renderCompany()
{
    $('.locations li > img').each(function(){
        var myParent = $(this).parent();
        $(this).css({
            "width": "auto",
            "height": "100%"
        });
        if ($(this).width() < myParent.width()) {
            $(this).css({
                "width": "auto",
                "height": "100%"
            });
        }
    });
}

function lastSlide(slider) {
    var total = slider.getSlideCount();
    var current = slider.getCurrentSlide() + 1;
    var lastslide = total / current;
    if (lastslide == 1) {
        $('#bottomCarousel .carousel-inner').addClass('endSlide');
    }else {
        $('#bottomCarousel .carousel-inner').removeClass('endSlide');
    }
}

function renderHome()
{
    //set topBanner height
    var winH = $(window).height();
    if ($('.companypage').length) {
        winH += 50;
    }
    var currentH = $('#topBanner .content h1').height();
    $('#topBanner').height(winH);
    
    var bottomPos = (winH - currentH)/2 - 10;
    $('#topBanner .content').css({
        'bottom': bottomPos + 'px'
    });
    
    $("#affixNav ul li a[href^='#']").on('click', function(e) {
       e.preventDefault();
       var hash = this.hash;
       $('html, body').animate({
           scrollTop: $(hash).offset().top
         }, 300, function(){
           window.location.hash = hash;
         });
    });
}

function addBIO(me)
{
    $('#bxslider-bio').remove();
    var bio = me.find('.bxslider-bio');
    var bioEL = $('<div></div>');
    bioEL.append(bio.html());
    bioEL.attr('id','bxslider-bio');
    bioEL.insertAfter(me.closest('.bx-viewport'));
}
function destroyBIO(slider)
{
    //$('#bxslider-bio').remove();
    $('#bxslider-close').remove();
    slider.children('.slide').removeClass('slide active-slide');
    slider.removeAttr('style');
    startSlider();
}
function startSlider()
{
    $(".bxslider li").each(function(index){
        $(this).attr('data-slide-index', index);
    });
    $(".bxslider li").on('click', function(){
        
        var me = $(this);
        var myParent = me.parent();
        var maxWidth = myParent.width();
        myParent.children('li').off("click").addClass('slide');
    
        var index = me.attr('data-slide-index');
        //slider.goToSlide(index);
        me.addClass('active-slide');
    
        var bioELClose = $('<a>close</a>');
        bioELClose.attr('id','bxslider-close');
        bioELClose.insertBefore(myParent);
        bioELClose.on('click', function(){
            destroyBIO(myParent);
        });
        
        var target = $("#management");
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
          $('html,body').animate({
            scrollTop: target.offset().top
          }, 1000);
        }
    });
}

function balanceHeight(classname)
{
    var maxheight='';
	$(classname).each(function(){
		if($(this).height() > maxheight)
		maxheight = $(this).height();
	});
    
    $(classname).each(function(){
		$(this).height(maxheight);
	});
}