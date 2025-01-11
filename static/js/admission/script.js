window.onload = (event) => {
let compulsory_subject_initialized=document.getElementsByClassName('selector-available');
let filter_compusory=document.getElementById('id_compulsory_subject_filter_selected');
let remove_compusory=document.getElementById('id_compulsory_subject_remove_all_link');

let selector_chooser=document.getElementsByClassName('selector-chooser');


compulsory_subject_initialized[0].style.display='none';
selector_chooser[0].style.display='none';

filter_compusory.style.display='none';
remove_compusory.style.display='none';

z= compulsory_subject_initialized.getElementsByTagName("option");
for (i = 0; i < z.length; i++) {

  z[i].setAttribute('disabled','true','readonly','true');

}

alert(compulsory_subject_initialized.length);
};




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
   let downloadDiv = document.getElementById('downlod_form_id');

   let addChoiceBtn=document.getElementsByName('id_fourth_subject');
   
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
    var x, y, i, valid = true;
    var options=document.getElementById('id_compulsory_subject_to').getElementsByTagName('option');
    for(i=0;i<options.length ;i++){
    options[i].selected = 'selected';
    }
    //document.getElementById('id_compulsory_subject_to').disabled='disabled';


          //document.getElementById('toast-container').style.visibility ='hidden';
      current_step++;
      let previous_step = current_step - 1;
      let flag=validateForm();
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
      if(current_step==4 ){
        

        if(document.getElementById('id_fourth_subject').value==''){
          valid= false;
        }
       /* var select=document.getElementsByName('compulsory_subject');
          var compulsory_subject=select[1];
          if(compulsory_subject.length<6){
            valid= false;
          }*/

        
          

      }
      
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
                   x.className = "toast-top-center";
                   x.style.visibility ="visible";

                   setTimeout(function(){ 
                       x.className = x.className.replace("toast-top-center","");
                       x.style.visibility ="hidden";

                       
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


/*submitBtn.addEventListener('click', () => {
    //preloader.classList.add('d-block');

     ///////////////////Submit student form Ajax code///////////////////

     var frm = $('#form-wrapper')[0];
     var form= new FormData(frm);

     var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

     // Get the data from the form
    

     // Send AJAX request
     $.ajax({
         enctype: 'multipart/form-data',
         type: 'POST',
         url: "{% url 'admission_form_submit' %}",  // Adjust the URL as per your project structure
         data: form1,
         headers: {
             'X-CSRFToken': csrfToken
         },
         
         cache:false,
         processData:false,
         contentType:false,
        
         success: function (response) {
             
             //document.getElementById("student_form").reset();
             if (response.status === 'success') {
                 // Clear the form
                
                alert(response.status);


             } else {
              alert("Success message not found");
                     
                 }
                 
         },
         error: function (xhr, status, error) {
            
             var err = eval("(" + xhr.responseText + ")");
             alert(err.Message);
         }
     });


    //////////////////////////////////////////////////////////////////
    const timer = ms => new Promise(res => setTimeout(res, ms));

    timer(3000)
      .then(() => {
           bodyElement.classList.add('loaded');
      }).then(() =>{
          step[stepCount].classList.remove('d-block');
          step[stepCount].classList.add('d-none');
          prevBtn.classList.remove('d-inline-block');
          prevBtn.classList.add('d-none');
          submitBtn.classList.remove('d-inline-block');
          submitBtn.classList.add('d-none');
          succcessDiv.classList.remove('d-none');
          succcessDiv.classList.add('d-block');
      })
      
});*/

function fourthSubject(id){
  alert(current_step);
  
  if(current_step==3){
    var compulsory_subject=document.getElementById('id_optional_subject_from');
    var selected_item = document.getElementById('id_fourth_subject');
      if(compulsory_subject.length==1){
        selected_item.value=compulsory_subject[0].value;
        return false;
      }

      
      
     
      

  }

}
function subjectChoice(id){
  alert("subjectChoice");

}
addChoiceBtn.addEventListener('change', () => {
    alert("subjectChoice");
});

