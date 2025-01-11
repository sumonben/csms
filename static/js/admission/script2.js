

const progress = (value) => {
   document.getElementsByClassName('progress-bar')[0].style.width = `${value}%`;
}

   let step = document.getElementsByClassName('step');
   let prevBtn = document.getElementById('prev-btn');
   let nextBtn = document.getElementById('next-btn');
   let submitBtn = document.getElementById('submit-btn');
   let form = document.getElementsByTagName('form')[0];
   let preloader = document.getElementById('preloader-wrapper');
   let bodyElement = document.querySelector('body');
   let succcessDiv = document.getElementById('success');
 
   form.onsubmit = () => { return false }

   let current_step = 0;
   let stepCount = 4
   step[current_step].classList.add('d-block');
   if(current_step == 0){
      prevBtn.classList.add('d-none');
      submitBtn.classList.add('d-none');
      nextBtn.classList.add('d-inline-block');
   }


   nextBtn.addEventListener('click', () => {
      //document.getElementById('toast-container').style.opacity =1;
      //document.getElementById('toast-container').style.visibility ='hidden';

      current_step++;
      let previous_step = current_step - 1;
      let flag=validateForm();
      //alert(go);

      if(( current_step > 0) && (current_step <= stepCount) && flag){
        prevBtn.classList.remove('d-none');
        prevBtn.classList.add('d-inline-block');
        step[current_step].classList.remove('d-none');
        step[current_step].classList.add('d-block');
        step[previous_step].classList.remove('d-block');
        step[previous_step].classList.add('d-none');
        if (current_step == stepCount){
          submitBtn.classList.remove('d-none');
          submitBtn.classList.add('d-inline-block');
          nextBtn.classList.remove('d-inline-block');
          nextBtn.classList.add('d-none');
        }
      } else {
        if(current_step > stepCount){
            form.onsubmit = () => { return true }
        }
      }
    progress((100 / stepCount) * current_step);
   
function validateForm() {
   // This function deals with validation of the form fields
   var x, y, i, valid = true;
   x = document.getElementsByClassName("step d-block");
   //alert(current_step);

   y = x[0].getElementsByTagName("input");
   z= x[0].getElementsByTagName("select");
   for (i = 0; i < y.length; i++) {
     // If a field is empty...
      //alert(y[i]+y[i].required);
//alert(y[i].getAttribute('id')+": "+y[i].hasAttribute('required'));

     if (y[i].value == '' && y[i].hasAttribute('required') ) {

      
         y[i].className='textfieldUSERinfoInvalid';

       valid = false;

     }
   }
   
   for (i = 0; i < z.length; i++) {
      // If a field is empty...

      if (z[i].value == '' && z[i].hasAttribute('required') ) {
         //alert(z[i].getAttribute('id')+": "+z[i].hasAttribute('required'));

        if(z[i].className=='textfieldUSER')
          z[i].className='textfieldUSERInvalid';
       else
         z[i].className='textfieldUSERinfoInvalid';
 
        valid = false;

      }
    }
   //alert("valid:"+valid);
   if(!valid){
      current_step--;
      var x = document.getElementById("toast-container");
                   x.style.visibility ="visible";
  // Add the "show" class to DIV
                x.className = "toast-top-center";

  // After 3 seconds, remove the show class from DIV
                setTimeout(function(){ 
                    x.className = x.className.replace("toast-top-center", "");
                    
                 }, 8000);
                 

   }
    return valid; // return the valid status
}



    });
    


   prevBtn.addEventListener('click', () => {
     if(current_step > 0){
        current_step--;
        let previous_step = current_step + 1; 
        prevBtn.classList.add('d-none');
        prevBtn.classList.add('d-inline-block');
        step[current_step].classList.remove('d-none');
        step[current_step].classList.add('d-block')
        step[previous_step].classList.remove('d-block');
        step[previous_step].classList.add('d-none');
        if(current_step < stepCount){
           submitBtn.classList.remove('d-inline-block');
           submitBtn.classList.add('d-none');
           nextBtn.classList.remove('d-none');
           nextBtn.classList.add('d-inline-block');
           prevBtn.classList.remove('d-none');
           prevBtn.classList.add('d-inline-block');
        } 
     }

     if(current_step == 0){
        prevBtn.classList.remove('d-inline-block');
        prevBtn.classList.add('d-none');
     }
    progress((100 / stepCount) * current_step);
   });


submitBtn.addEventListener('click', () => {
   for(var i=0; i < form.elements.length; i++){
      if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
         form.elements[i].className='textfieldUSERinfoInvalid';
        alert('There are some required fields!');
        return false;
      }
    }
    form.submit();
    preloader.classList.add('d-block');

    const timer = ms => new Promise(res => setTimeout(res, ms));

    timer(3000).then(() => {
           bodyElement.classList.add('loaded');
      }).then(() =>{
         alert("working ");
          step[stepCount].classList.remove('d-block');
          step[stepCount].classList.add('d-none');
          prevBtn.classList.remove('d-inline-block');
          prevBtn.classList.add('d-none');
          submitBtn.classList.remove('d-inline-block');
          submitBtn.classList.add('d-none');
          succcessDiv.classList.remove('d-none');
          succcessDiv.classList.add('d-block');
      })
      
});

