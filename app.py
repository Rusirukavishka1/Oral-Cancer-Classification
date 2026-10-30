from pathlib import Path
import hashlib
import json
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Oral Cancer | Research Observatory', page_icon='◈', layout='wide')
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
html,body,[class*="css"],.stApp{font-family:'DM Sans',sans-serif;}
.stApp{background:radial-gradient(ellipse at 95% 0%,#dceeff 0%,transparent 45%),linear-gradient(145deg,#f8fbff,#edf4fb);color:#142943;}
[data-testid="stSidebar"]{background:linear-gradient(175deg,#0b2346,#123b68);}
[data-testid="stSidebar"] *{color:#edf5ff!important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#bdd4ef!important;}
.block-container{padding-top:2.5rem;max-width:1450px;}
h1{font-weight:700!important;letter-spacing:-1.3px!important;color:#102d50!important;}
h2,h3{color:#153456!important;}
[data-testid="stMetric"]{background:rgba(255,255,255,.92);border:1px solid #dce7f4;border-radius:16px;padding:20px;box-shadow:0 8px 24px #16396008;}
[data-testid="stMetricValue"]{color:#1363ba;}
.hero{background:linear-gradient(115deg,#0b2a51,#165d9f);border-radius:22px;padding:32px 36px;color:white;margin:12px 0 24px;box-shadow:0 12px 35px #133d7120;}
.hero h2{color:white!important;font-size:1.8rem;margin:6px 0 12px;}
.hero p{color:#daebff;max-width:850px;line-height:1.65;}
.eyebrow{font-size:11px;letter-spacing:2.5px;font-weight:700;color:#8fcbff;}
.note{border-left:4px solid #e3aa37;background:#fff8e8;padding:17px 22px;border-radius:8px;color:#694b14;margin:18px 0;line-height:1.6;}
.footer{border-top:1px solid #d8e5f2;padding-top:18px;margin-top:30px;color:#61748a;font-size:12px;}
.stButton>button,.stDownloadButton>button{border-radius:10px;}
</style>''', unsafe_allow_html=True)

@st.cache_data
def load_bundle():
    meta = json.loads((ROOT/'data/provenance.json').read_text(encoding="utf-8-sig"))
    content = (ROOT/'data/oral_cancer_prediction_dataset.csv').read_bytes()
    if hashlib.sha256(content).hexdigest() != meta['dataset_sha256']:
        raise ValueError('Dataset changed. The saved model results belong to the bundled dataset; restore it before continuing.')
    df = pd.read_csv(ROOT/'data/oral_cancer_prediction_dataset.csv')
    summary = pd.read_csv(ROOT/'data/model_summary.csv').set_index('Model')
    folds = pd.read_csv(ROOT/'data/fold_results.csv')
    reports = (ROOT/'data/reports.txt').read_text(encoding="utf-8-sig")
    if len(df)!=meta['rows'] or len(summary)!=4 or len(folds)!=48:
        raise ValueError('Result bundle is incomplete or inconsistent.')
    return df,summary,folds,reports,meta
try:
    df,summary,folds,reports,meta = load_bundle()
except (OSError, ValueError, KeyError, pd.errors.ParserError) as e:
    st.error(f'Unable to load the verified research bundle: {e}')
    st.info('Extract the entire ZIP, including data/ and assets/, and run app.py again.')
    st.stop()

TARGET = 'Oral Cancer (Diagnosis)'
COLORS = ['#1769bf','#38a5c9','#8599bd','#153959']
MODELS = summary.index.tolist()
BASELINE = df[TARGET].eq('No').mean()

def chart(fig):
    fig.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family='Arial',color='#23415e'),margin=dict(l=10,r=15,t=45,b=15),legend_title_text='')
    st.plotly_chart(fig,width='stretch')

def asset(name, caption):
    path = ROOT/'assets'/f'{name}.png'
    if path.exists():st.image(str(path),caption=caption,width='stretch')
    else:st.warning(f'Missing chart: {name}.png. Restore the assets folder.')

def hero(kicker,title,body):
    st.markdown(f'<div class="hero"><div class="eyebrow">{kicker}</div><h2>{title}</h2><p>{body}</p></div>',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('## ◈ Research\nObservatory')
    st.caption('ORAL CANCER CLASSIFICATION')
    st.divider()
    page=st.radio('Explore the study',['Overview','Dataset explorer','Model comparison','Classification reports','Training & trees','Methodology'],label_visibility='collapsed')
    st.divider()
    st.markdown('**VERIFIED RUN**\n\n84,922 observations\n\n15 candidate features\n\n12 stratified folds\n\n4 model families')
    st.caption('Saved research results • No retraining on navigation')

st.caption('GROUP C  /  MACHINE LEARNING RESEARCH')
st.title(page)
if page=='Overview':
    hero('EVIDENCE BEFORE ACCURACY','A clearer view of the experiment.',
         'Explore the corrected classification study, its dataset and the results of four models evaluated on identical cross-validation folds.')
    cols=st.columns(4)
    for col,label,value in zip(cols,['Observations','Candidate features','CV folds','Model families'],['84,922','15','12','4']):col.metric(label,value)
    st.markdown('<div class="note"><b>Limited predictive signal.</b> OOF accuracies range from 49.67% to 50.18%. Always predicting the majority class would score 50.13%. These results do not establish useful diagnostic performance.</div>',unsafe_allow_html=True)
    a,b=st.columns([1.6,1])
    with a:
        st.subheader('Model accuracy in context')
        fig=px.bar(summary.reset_index(),x='Model',y='OOF Accuracy',color='Model',color_discrete_sequence=COLORS)
        fig.add_hline(y=BASELINE,line_dash='dot',line_color='#bb8330',annotation_text='Majority-class reference: 50.13%')
        fig.update_yaxes(range=[0,1],tickformat='.0%');fig.update_layout(showlegend=False);chart(fig)
    with b:
        st.subheader('Diagnosis distribution')
        counts=df[TARGET].value_counts().rename_axis('Diagnosis').reset_index(name='Records')
        fig=px.pie(counts,names='Diagnosis',values='Records',hole=.72,color='Diagnosis',color_discrete_map={'No':'#1769bf','Yes':'#8dc8ef'})
        fig.update_traces(textinfo='percent+label');chart(fig)
    st.caption('The majority-class reference is calculated from observed class prevalence; it is not an additional trained model.')

elif page=='Dataset explorer':
    hero('SOURCE DATA','Inspect the population behind the scores.', 'Filters below affect exploratory data views only. Saved model evaluations always cover the complete dataset.')
    a,b,c=st.columns(3)
    with a:countries=st.multiselect('Country',sorted(df['Country'].unique()),placeholder='All countries')
    with b:diagnosis=st.selectbox('Recorded diagnosis',['All','Yes','No'])
    with c:ages=st.slider('Age range',int(df.Age.min()),int(df.Age.max()),(int(df.Age.min()),int(df.Age.max())))
    selected=df[df.Age.between(*ages)]
    if countries:selected=selected[selected.Country.isin(countries)]
    if diagnosis!='All':selected=selected[selected[TARGET].eq(diagnosis)]
    st.metric('Records in current view',f'{len(selected):,}')
    if selected.empty:st.info('No records match these filters. Broaden the selection.')
    else:
        feature=st.selectbox('Explore a column',[c for c in df.columns if c!='ID'])
        if pd.api.types.is_numeric_dtype(selected[feature]):
            fig=px.histogram(selected,x=feature,nbins=30,color_discrete_sequence=['#277ec8'])
        else:
            counts=selected[feature].value_counts().rename_axis(feature).reset_index(name='Records')
            fig=px.bar(counts,x=feature,y='Records',color_discrete_sequence=['#277ec8'])
        chart(fig)
        st.caption('Raw values are preserved, including valid zeros. Treatment and outcome fields are displayed for exploration but excluded from model inputs.')
        st.dataframe(selected.head(500),width='stretch',hide_index=True)
        st.caption('Preview limited to the first 500 matching records. Download includes all matching records.')
        st.download_button('Download filtered records',selected.to_csv(index=False).encode(),'filtered_records.csv','text/csv')
    with st.expander('Full-dataset candidate feature correlations'):asset('correlations','Saved corrected notebook heatmap — descriptive associations, not causal effects.')

elif page=='Model comparison':
    hero('OUT-OF-FOLD EVALUATION','Compare like with like.', 'Every model uses the same 15 inputs and 12 folds. Each record is evaluated once by a model that did not train on that record.')
    selected_models=st.multiselect('Models',MODELS,default=MODELS)
    metric=st.selectbox('Metric',['Accuracy','Precision','Recall','F1'])
    if selected_models:
        filtered=summary.loc[selected_models]
        fig=px.bar(filtered.reset_index(),x='Model',y='OOF '+metric,color='Model',color_discrete_sequence=COLORS)
        fig.update_yaxes(range=[0,1],tickformat='.0%');fig.update_layout(showlegend=False);chart(fig)
        st.subheader('Performance across folds')
        chart(px.line(folds[folds.Model.isin(selected_models)],x='Fold',y=metric,color='Model',markers=True,color_discrete_sequence=COLORS).update_yaxes(range=[0,1],tickformat='.0%'))
        st.dataframe(filtered.style.format('{:.2%}'),width='stretch')
        agg=folds[folds.Model.isin(selected_models)].groupby('Model')[metric].agg(['mean','std'])
        st.caption('Fold mean and standard deviation below describe variation; standard deviation is not a confidence interval.')
        st.dataframe(agg.style.format('{:.4f}'),width='stretch')
    else:st.info('Select at least one model to compare.')
    st.download_button('Download pooled OOF metrics',summary.to_csv().encode(),'oof_metrics.csv','text/csv')
    st.download_button('Download all fold results',folds.to_csv(index=False).encode(),'fold_results.csv','text/csv')
    st.caption(meta['metrics_precision']+' Cancer (1) is the positive class. Undefined precision is reported as 0, matching the notebook.')

elif page=='Classification reports':
    hero('LOOK BEYOND ACCURACY','See the errors each model makes.', 'Pooled reports and confusion matrices cover all 84,922 out-of-fold predictions. They are not limited to the final fold.')
    model=st.selectbox('Choose a model',MODELS)
    cols=st.columns(4)
    for col,metric in zip(cols,['Accuracy','Precision','Recall','F1']):col.metric(metric,f'{summary.loc[model,"OOF "+metric]:.2%}')
    if model=='Decision Tree':st.warning('This fixed Decision Tree predicts only No Cancer. Cancer recall is 0%; majority-class accuracy hides this failure.')
    marker=model+' — pooled out-of-fold classification report'
    _, found, part = reports.partition(marker)
    if found:
        for other in MODELS:
            next_marker = other + ' — pooled out-of-fold classification report'
            part = part.split(next_marker, 1)[0]
        st.code(part.strip(), language='text')
    else:
        st.error(f'Classification report for {model} could not be found.')
        st.info('Restore the original data/reports.txt file from the dashboard package.')
    with st.expander('Reading the report',expanded=False):
        st.write('Precision: among Cancer predictions, the fraction labeled Cancer. Recall: among records labeled Cancer, the fraction detected. F1 balances precision and recall. Support is the number of records in each class.')
    asset('confusion_matrices','All four models • rows = actual class, columns = predicted class • pooled OOF predictions')

elif page=='Training & trees':
    hero('MODEL DIAGNOSTICS','Understand what was fitted.', 'View the saved ANN training histories and tree structures from the corrected notebook. These are research diagnostics, not deployed prediction models.')
    view=st.selectbox('Visualization',['ANN loss','Decision Tree','Random Forest tree'])
    if view=='ANN loss':
        asset('ann_loss','Complete 5-epoch training loss histories for all 12 folds.')
        st.info('The outer test folds were not used as training validation data. No validation-loss curve is available. Low training loss alone does not establish generalization.')
        st.code('15 inputs → Dense(8, ReLU) → Dropout(0.5)\n→ Dense(4, ReLU) → Dropout(0.5) → Dense(1, Sigmoid)\nAdam · Binary cross-entropy · 5 epochs · batch size 256',language='text')
    elif view=='Decision Tree':
        asset('decision_tree','Final CV fold only. This tree is not refitted on the complete dataset.')
        st.write('Original settings retained: max_depth=4, min_samples_split=20, min_samples_leaf=10, max_leaf_nodes=10, max_features=0.5, ccp_alpha=0.01.')
    else:
        asset('random_forest_tree','First tree of the final-fold forest. Display truncated to depth 3; thresholds use standardized inputs.')
        st.write('Original settings retained: 20 estimators, max_depth=12, random_state=42.')

else:
    hero('TRANSPARENT METHODS','Know what these results can support.', 'The study assumes prediction before diagnosis and treatment. Only candidate information available at that moment belongs in the feature matrix.')
    st.subheader('What changed')
    st.markdown('''- Valid zeros are preserved; no whole-dataset mean imputation.
- Categories are checked explicitly; numeric workdays are not silently mapped to zero.
- All models use the same candidate inputs and identical stratified folds.
- Scaling is fitted only on the training fold.
- ANN layer construction is corrected and each fold is trained once.
- Reports aggregate out-of-fold predictions across every row.''')
    st.subheader('Excluded from model inputs')
    st.dataframe(pd.DataFrame({'Field':['ID / Country','Treatment Type / Treatment Cost','Cancer Stage / Early Diagnosis','Tumor Size','5-year Survival Rate / Lost Workdays'],
        'Reason':['ID and Country excluded as in the original assignment','Treatment information may reveal an already-known diagnosis','Diagnosis-related information excluded under the task assumption','Availability before diagnosis was not established','Later outcomes do not belong in a pre-diagnosis prediction']}),hide_index=True,width='stretch')
    st.subheader('Limits of the study')
    st.write('Source provenance, patient-group structure and collection timing were not supplied. Unique IDs do not prove independent patients. The fixed settings were not tuned and there is no independent external test cohort. Dataset associations do not establish clinical validity. Near-50% results do not demonstrate useful discrimination.')
    st.info('This dashboard presents research evidence. It does not generate patient diagnoses or risk scores.')
    with st.expander('Reproducibility and source fingerprints'):
        st.json(meta)
        st.write('All notebook code cells were executed sequentially in a fresh IPython process. All 48 fold fits completed. Windows/Anaconda execution was not tested.')
    notebook=ROOT/'finished_assignment_corrected.ipynb'
    if notebook.exists():st.download_button('Download the corrected notebook',notebook.read_bytes(),notebook.name,'application/x-ipynb+json')

st.markdown('<div class="footer">ORAL CANCER · RESEARCH OBSERVATORY &nbsp; / &nbsp; Saved corrected-notebook results &nbsp; / &nbsp; Educational analysis</div>',unsafe_allow_html=True)
