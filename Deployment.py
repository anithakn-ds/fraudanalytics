import streamlit as st 
import pandas as pd
from pickle import dump
from pickle import load
from PIL import Image
import sklearn
import base64

from load_css import local_css

local_css("style.css")

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        padding-top: 0rem;
    }}
   
</style>
""",
        unsafe_allow_html=True,
    )

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    width: auto;
    height: auto;
    }
  }
    
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
                                      
set_background('insurance-1.jpeg')

                                      


col1, col2 = st.beta_columns(2)

names = "<div><span class='red_heading'>Fraud Analytics</span></div>"
col1.markdown(names, unsafe_allow_html=True)

image = Image.open('excelr.png')
col2.image(image, caption=None, width=200, use_column_width=None, clamp=False, channels='RGB', output_format='auto')

#st.title('Model Deployment: Random Forest')
st.sidebar.header('User Input Parameters')

age_display = ("0 to 17","18 to 29","30 to 49","50 to 69","70 or Older")
options1 = list(range(len(age_display)))

surg_display = ("Medical","Surgical")
options2 = list(range(len(surg_display)))

emerg_display = ("Yes","No")
options3 = list(range(len(emerg_display)))

adm_display = ("Elective","Emergency","New Born","Not Available","Trauma","Urgent")
options4 = list(range(len(adm_display)))

care_display = ("Another Type","Cancer Center","Court/Law Enforcement","Critical Access","Expired","Facility","Federal","Home/Self care","HHS","Hosp-Medicare","Hospice-Home","Hospice-Medical","Inpatient","Left-Advice","MedicAid-Nursing","Medicare-Long Term","Psychiatric","Short-term","Skilled")
options5 = list(range(len(care_display)))


def user_input_features():
    
    age = st.sidebar.selectbox("Age", options1, format_func=lambda x: age_display[x])
    days_spent = st.sidebar.number_input("Days Spent(1 to 120 days)",min_value=1, max_value=120)
    admission_type = st.sidebar.selectbox('Admission Type',options4, format_func=lambda x: adm_display[x])
    home_self = st.sidebar.selectbox('Home/Self care',options5, format_func=lambda x: care_display[x])
    diagnosis_code = st.sidebar.number_input("Diagnosis Code",min_value=1, max_value=670,format="%i")
    procedure_code = st.sidebar.number_input("Procedure Code",min_value=0, max_value=231,format="%i")
    code_illness = st.sidebar.selectbox('Code Illness',('1','2','3','4'))
    mortality_risk = st.sidebar.selectbox('Mortality Risk',('1','2','3','4'))
    surg_description = st.sidebar.selectbox('Surgical Description',options2, format_func=lambda x: surg_display[x])
    emergency = st.sidebar.selectbox('Emergency Yes/No',options3, format_func=lambda x: emerg_display[x])
    tot_charge = st.sidebar.number_input("Total Charge")
    tot_cost = st.sidebar.number_input("Total Cost")
    ratio = st.sidebar.number_input("Ratio")
    #payment_typology = st.sidebar.selectbox('Payment',('1','2','3','4'))
    
   
    data = {
            'AGE':age,
            'DAYS_SPENT':days_spent,
            'ADMISSION_TYPE':admission_type,
            'HOME_SELF CARE':home_self,
            'DIAGNOSIS CODE':diagnosis_code,
            'PROCEDURE CODE':procedure_code,
            'CODE ILLNESS':code_illness,
            'MORTALITY RISK':mortality_risk,
            'SURGICAL DESC':surg_description,
            'EMERGENCY':emergency,
            'TOTAL CHARGE':tot_charge,
            'TOTAL COST':tot_cost,
            'RATIO':ratio
            #'PAYMENT':payment_typology
           }
    
    features = pd.DataFrame(data,index = [0])
    return features 
    
names = "<div><span class='blue'>Anitha-Jinson-Pranav-Santhosh-Vishal-Shriniwas</span></div>"
st.markdown(names, unsafe_allow_html=True)

df_depl = user_input_features()
st.subheader('User Input parameters')
#st.write(df_depl,unsafe_allow_html=True)

col3, col4 = st.beta_columns(2)

if (df_depl.iloc[0][0]==0):
   col3.markdown("Age-0 to 17 yrs")
elif(df_depl.iloc[0][0]==1):
    col3.markdown("Age-18 to 29 yrs")
elif(df_depl.iloc[0][0]==2):
    col3.markdown("Age-30 to 49 yrs")
elif(df_depl.iloc[0][0]==3):
    col3.markdown("Age-50 to 69 yrs")
elif(df_depl.iloc[0][0]==4):
    col3.markdown("Age-70 and Older")
    
var_1 = df_depl.iloc[0][4]
md_results = f"**{var_1:.2f}**"

col4.markdown("Days Spent - "+f"**{df_depl.iloc[0][1]: 2d}**")

if (df_depl.iloc[0][2]==0):
   col3.markdown("Admission Type-Elective")
elif(df_depl.iloc[0][2]==1):
    col3.markdown("Admission Type-Emergency")
elif(df_depl.iloc[0][2]==2):
    col3.markdown("Admission Type-New Born")
elif(df_depl.iloc[0][2]==3):
    col3.markdown("Admission Type-Not Available")
elif(df_depl.iloc[0][2]==4):
    col3.markdown("Admission Type-Trauma")
elif(df_depl.iloc[0][2]==4):
    col3.markdown("Admission Type-Urgent")
    
col4.markdown("Home/Self Care - "+f"**{df_depl.iloc[0][3]:2d}**")
    
col3.markdown("Diagnostic Code - "+f"**{df_depl.iloc[0][4]:2d}**")
col4.markdown("Procedure Code - "+f"**{df_depl.iloc[0][5]: 2d}**")

col3.markdown("Code Illeness - "+f"**{int(df_depl.iloc[0][6]):2d}**")
col4.markdown("Mortality Risk - "+f"**{int(df_depl.iloc[0][7]):2d}**")

if (df_depl.iloc[0][8]==0):
    col3.markdown("Surgical Description - Medical")
else:
    col3.markdown("Surgical Description - Surgical")
    
if (df_depl.iloc[0][9]==0):
    col4.markdown("Emergency")
else:
    col4.markdown("Not Emergency")
    
col3.markdown("Total Charge - "+f"**{df_depl.iloc[0][10]:.2f}**")
col4.markdown("Total Cost - "+f"**{df_depl.iloc[0][11]:.2f}**")

col3.markdown("Ratio - "+f"**{df_depl.iloc[0][12]:.2f}**")

# load the model from disk
#loaded_model = load(open('Model_final.joblib', 'rb'))
loaded_model = load(open('Model.joblib', 'rb'))


prediction = loaded_model.predict(df_depl)
prediction_proba = loaded_model.predict_proba(df_depl)

st.markdown("<div><span class='pred_result'>Predicted Result</span></div>",unsafe_allow_html=True)
st.markdown("<div><span class='green'>Genuine</span></div>" if prediction_proba[0][1] > 0.55 else "<div><span class='red'>Fraud</span></div>",unsafe_allow_html=True)

st.markdown("<div><span class='pred_result'>Prediction Probability</span></div>",unsafe_allow_html=True)
#st.write(prediction_proba)

col5, col6 = st.beta_columns(2)

col5.markdown("Probability-Fraud - "+str(prediction_proba[0][0]))
col6.markdown("Probability-Genuine - "+str(prediction_proba[0][1]))


