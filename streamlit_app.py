import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
from PyPDF2 import PdfWriter, PdfReader

figures = []
# read the csv that was preprocessed in jupyter file
df = pd.read_csv("final_df.csv")
st.markdown("<h1 style='text-align: center; color: white;'>Exploratary Data Analysis (EDA)</h1>",
            unsafe_allow_html=True)
fig = plt.figure(figsize=(18, 12))
ax = fig.gca()
df.hist(ax=ax)
plt.suptitle('Histogram for the Distribution of Numerical Features\n\n',
             fontsize=30, color='teal')
figures.append(fig)
st.pyplot(fig)

for col in df.select_dtypes(include='object'):
    if df[col].nunique() <= 12:
        i = plt.figure(figsize=(12, 8))
        sns.countplot(y=col, data=df)
        st.pyplot(i)
        figures.append(i)

# 2) which gender comes to the laundry shop more
new_df = df.copy()
fig = plt.figure(figsize=(12, 8))
ax = sns.countplot(x=new_df["Gender"], palette='Pastel1',
                   order=new_df["Gender"].value_counts().index)
for container in ax.containers:
    ax.bar_label(container)
plt.title("Findings: From the plot above, we can see the female tends to visit the laundry shop more.",
          y=-0.12,  fontsize=12)
plt.suptitle('Which Gender visits the Self Laundry Shop more?',
             fontsize=18, color='teal')
st.pyplot(fig)
figures.append(fig)

# 3) What types of customers are more likely to choose Washer No.X and Dryer No.Y?
fig = plt.figure(figsize=(12, 10))
ax = sns.countplot(x='Washer_No', data=new_df, hue="Dryer_No", palette='magma')
for container in ax.containers:
    ax.bar_label(container)

sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.suptitle('What type of customers are more likely to choose Washer No.X and Dryer No.Y?',
             fontsize=18, color='teal')
plt.title('Findings: From the grouped bar plot, we can see that for Washer No (3,4,6), \ncustomers are more likely to use Dryer_no 7 while for Washer No 5,\n customers are more likely to use Dryer_No 9.\n \n Thus, we will dive more into the types of customers choosing the highest and\n lowest frequency of choosing the corresponding washer and dryer in the next section:\n a) Highest frequency of customers choosing Washer_No.3 and Dryer_No.7 : 281\n b) Lowest frequency of customers choosing Washer_No.3 and Dryer_No.10 : 224', y=-0.5, fontsize=15)
plt.tight_layout()
st.pyplot(fig)
figures.append(fig)

df2 = new_df.copy()

#dryer, washer


def washer_dryer(x, y, df2copy, c, p):
    # Get only rows with corresponding washer and dryer
    df2copy = df2copy.loc[(df2copy["Washer_No"] == x) &
                          (df2copy["Dryer_No"] == y)]
    fig = plt.figure(figsize=(12, 10))
    # Pie chart according to Race
    data = df2copy['Race'].value_counts()
    label = df2copy['Race'].value_counts().index
    plt.pie(data, labels=label, autopct='%1.1f%%', explode=[
            0.05]*4, textprops={'fontsize': 14}, colors=c),
    plt.suptitle("What types of customers are more likely to choose Washer No." + str(x) + " and Dryer No." + str(y) +
                 "\n\n Race of Customers choosing Washer No." + str(x) + " and Dryer No." + str(y), fontsize=18, color='teal')
    st.pyplot(fig)
    figures.append(fig)

    # Grouped barplot not considering gender
    fig = plt.figure(figsize=(12, 10))
    fig = sns.catplot(data=df2copy, kind="bar", x="Race", y="Age_Range", hue="Body_Size", palette="dark", alpha=.6, height=5).set(
        title="Customers choosing Washer No." + str(x) + " and Dryer No." + str(y) + " (Without considering gender)")

    fig.despine(left=True)
    fig.set_axis_labels("", "Age")
    fig.legend.set_title("")
    plt.tight_layout()
    st.pyplot(fig)
    figures.append(fig)
    # set colours
    clrs = ["#4374B3", "#d68fb3"]
    sns.set_palette(sns.color_palette(clrs))

    fig = plt.figure(figsize=(12, 10))

    # Grouped barplot considering gender
    fig = sns.catplot(x="Race", y="Age_Range", hue="Body_Size", col="Gender",
                      palette=p, data=df2copy, kind="bar", height=4, aspect=.8)

    fig.fig.subplots_adjust(top=0.75)
    fig.fig.suptitle("Customers choosing Washer No. " + str(x) +
                     " and Dryer No." + str(y) + " (Considering gender)", fontsize=18, color='teal')

    plt.title('Findings: \n i) The majority of ethnicity of people who chose Washer No.3 and\n Dryer No.7 are as followed : Malay, Indian, Chinese, and Foreigners. \n \n ii) Without considering the gender, customers who mostly chose Washer No.3 and \n  Dryer No.7 are people of Chinese ethnicity with *fat Body_Size* within the age group\n of 35-45. \n\n iii)  Considering the gender, for male, people of Chinese and Malay ethnicity *fat Body_Size* \n tends to choose Washer No.3 and Dryer No.7 whereas for female, Chinese with \n *thin Body_Size* tends to choose Washer No.3 and Dryer No.7', x=-0.3, y=-1.4, fontsize=15)
    plt.tight_layout()
    st.pyplot(fig)
    figures.append(fig)


def washer_dryer2(x, y, df2copy, c, p):
    # Get only rows with corresponding washer and dryer
    df2copy = df2copy.loc[(df2copy["Washer_No"] == x) &
                          (df2copy["Dryer_No"] == y)]
    fig = plt.figure(figsize=(12, 10))
    # Pie chart according to Race
    data = df2copy['Race'].value_counts()
    label = df2copy['Race'].value_counts().index
    plt.pie(data, labels=label, autopct='%1.1f%%', explode=[
            0.05]*4, textprops={'fontsize': 14}, colors=c),
    plt.suptitle("What types of customers are more likely to choose Washer No." + str(x) + " and Dryer No." + str(y) +
                 "\n\n Race of Customers choosing Washer No." + str(x) + " and Dryer No." + str(y), fontsize=18, color='teal')
    st.pyplot(fig)
    figures.append(fig)

    # Grouped barplot not considering gender
    fig = plt.figure(figsize=(12, 10))
    fig = sns.catplot(data=df2copy, kind="bar", x="Race", y="Age_Range", hue="Body_Size", palette="dark", alpha=.6, height=5).set(
        title="Customers choosing Washer No." + str(x) + " and Dryer No." + str(y) + " (Without considering gender)")

    fig.despine(left=True)
    fig.set_axis_labels("", "Age")
    fig.legend.set_title("")
    st.pyplot(fig)
    figures.append(fig)
    # set colours
    clrs = ["#4374B3", "#d68fb3"]
    sns.set_palette(sns.color_palette(clrs))

    fig = plt.figure(figsize=(12, 10))

    # Grouped barplot considering gender
    fig = sns.catplot(x="Race", y="Age_Range", hue="Body_Size", col="Gender",
                      palette=p, data=df2copy, kind="bar", height=4, aspect=.8)

    fig.fig.subplots_adjust(top=0.75)
    fig.fig.suptitle("Customers choosing Washer No. " + str(x) +
                     " and Dryer No." + str(y) + " (Considering gender)", fontsize=18, color='teal')

    plt.title('Findings: \n i) The majority of ethnicity of people who chose Washer No.3 and\n Dryer No.10 are as followed : Indian, Malay, Chinese and Foreigners. \n \n ii) Without considering the gender, customers who mostly chose Washer No.3 and \n  Dryer No.10  are Foreigners and people of Malay ethnicity with thin Body_Size,\n all which are mostly within the age group of 35-45. \n\n iii)  Considering the gender, for male, people of Indian ethnicity with thin Body_Size \n tends to choose Washer No.3 and Dryer No.10 whereas for female,\n people of Malay and Chinese ethnicity with moderate Body_Size as well \n as Foreigners with thin Body_Size tends to choose Washer No.3 and Dryer No.10.', x=-0.3, y=-1.5, fontsize=15)
    plt.tight_layout()
    st.pyplot(fig)
    figures.append(fig)


df2copy = df2.copy()
c = ["#845EC2", "#D65DB1", "#FF6F91", "#FF9671"]
p = "Set2"
washer_dryer(3, 7, df2copy, c, p)

c = ["#E18392", "#BC7699", "#926C97", "#938fae"]
p = "blend:#7AB,#EDA"
washer_dryer2(3, 10, df2copy, c, p)

# 4) Which age group tends to visit the self-service laundry shop more often?
bins = [10, 20, 30, 40, 50, 60]
df4 = new_df.copy()
fig = plt.figure(figsize=(12, 10))
df4['Age_Group'] = pd.cut(df4['Age_Range'], bins=bins)
ax = sns.countplot(x='Age_Group', data=df4, palette="rocket")
for container in ax.containers:
    ax.bar_label(container)
plt.suptitle('Which age group tends to visit the self-service laundry shop more often?',
             fontsize=18, color='teal')
plt.title('Findings: We can see from the barplot above that the age group between (30-40] \n tends to visit the self-service laundry shop more frequently, whereas the age group between\n (10-20] is less likely to visit the shop. ', y=-0.25, fontsize=15)
plt.tight_layout()
st.pyplot(fig)
figures.append(fig)

# Do customers with bigger body size tend to buy more drinks?
fig = plt.figure(figsize=(12, 8))
colors = ["#E18392", "#BC7699", "#926C97"]
plt.pie(new_df['Body_Size'].value_counts().values, labels=new_df['Body_Size'].value_counts().index,
        autopct='%1.1f%%', textprops={'fontsize': 12}, colors=colors), plt.title("Body_Size", fontdict={'fontsize': 15})
plt.suptitle('Do customers with bigger body size tend to buy more drinks?',
             fontsize=25, color='teal')
st.pyplot(fig)
figures.append(fig)


df8 = new_df.copy()
fig = plt.figure(figsize=(12, 6))
plt.suptitle('Bigger Body Size, Buy More Drinks?', fontsize=30, color='teal')
plt.subplot(121), sns.barplot(data=df8, x='Body_Size',
                              y='buyDrinks', palette='spring')
plt.subplot(122), sns.lineplot(
    data=df8, x='Body_Size', y='buyDrinks', alpha=0.5)
plt.title('\nFindings: Customers who are in a bigger body size, tend to buy more drinks in the laundry shop',
          x=-0.25, y=-0.25, fontsize=15)
plt.tight_layout()
st.pyplot(fig)
figures.append(fig)

# Create a button that, when clicked, will save the figure as a PDF
if st.button('Download as PDF'):
    # # Code to save the figure as a PDF
    # with open("figure.pdf", "wb") as f:
    #     plt.savefig(f, format="pdf")

    pdf_pages = []
    for i, fig in enumerate(figures):
        # Save the figure to a pdf file
        with open("figure_{}.pdf".format(i), "wb") as f:
            fig.savefig(f, format="pdf")
        pdf_file = open("figure_{}.pdf".format(i), "rb")
        # Read the pdf file and add it to the list of pages
        pdf_pages.append(PdfReader(pdf_file))
        # pdf_file.close()

    # Create a new pdf file
    output = PdfWriter()

    # Add all the pages from the list to the pdf file
    for page in pdf_pages:
        output.add_page(page.pages[0])

    with open("EDA.pdf", "wb") as outputStream:
        output.write(outputStream)
    output.close()

    # with open("temp.md", "w") as f:
    #     st.write(f, unsafe_allow_html=True)
    # st.success("Markdown written to temp.md")

    # # Use pandoc to convert the markdown file and figures pdf to a single pdf
    # subprocess.run(['pandoc', 'temp.md', 'combined_figures.pdf', '-o', 'output.pdf'])
    # st.success("Download Complete. Check the current working directory for output.pdf")
# pdf_pages = []
# for i in range(len(figures)):
#     pdf_pages.append(PdfFileReader(open("figure_"+str(i)+".pdf", "rb")))

# output = PdfFileWriter()
# for page in pdf_pages:
#     output.addPage(page.getPage(0))

# with open("combined_figures.pdf", "wb") as outputStream:
#     output.write(outputStream)


# prediction function with user input
def prediction(classifier, lat, long, age, attire, pants, time, basket, shirt, spent, basket_size):
    attire_dict = {'Casual': 0, 'Formal': 2, 'Traditional': 1}
    pants_dict = {'Black': 0, 'Blue': 1, 'Blue Jeans': 2, 'Grey': 5, 'Brown': 3, 'Red': 9, 'White': 10, 'Purple': 8, 'Orange': 6,
                  'Pink': 7, 'Green': 4, 'Yellow': 11}
    basket_col_dict = {'Black': 0, 'Blue': 1, 'Grey': 4, 'Brown': 2, 'Red': 8, 'White': 9, 'Purple': 7, 'Orange': 10,
                       'Pink': 6, 'Green': 3, 'Yellow': 5}
    shirt_dict = {'Black': 0, 'Blue': 1, 'Grey': 4, 'Brown': 2, 'Red': 8, 'White': 9, 'Purple': 7, 'Orange': 5,
                  'Pink': 6, 'Green': 3, 'Yellow': 10}
    basket_size_dict = {'Big': 0, 'Small': 1}
    attire2 = attire_dict.get(attire)
    pants2 = pants_dict.get(pants)
    basket2 = basket_col_dict.get(basket)
    shirt2 = shirt_dict.get(shirt)
    size2 = basket_size_dict.get(basket_size)
    prediction = classifier.predict(
        [pd.to_numeric([lat, long, age, attire2, pants2, time, basket2, shirt2, spent, size2])])
    if prediction == 1:
        predict = "Yes"
    else:
        predict = "No"
    return predict


# main function for webpage
def main():
    # title
    # load the models from the file
    pickle_in_st = open('lr.pkl', 'rb')
    # pickle_in_dt = open('DT.pkl', 'rb')
    stack = pickle.load(pickle_in_st)
    st.title("Prediction based on the variables for the Self-Service Laundry Shop")
    df = pd.read_csv("final_df.csv")

    def plotDot(point):
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            radius=2,
                            weight=5).add_to(map)

    # frontend design
    design = """
    <div style ="background-color:#CCCCFF;padding:13px">
    <h1 style ="color:black;text-align:center;">Classification</h1>
    </div>
    """

    # display the front end design
    st.markdown(design, unsafe_allow_html=True)

    # # drop down list to select classifier
    # option = st.selectbox(
    #  'Classifier',
    #  ('Decision Tree', 'Logistic Regression'))
    df_locations = df[["latitude", "longitude"]]
    locationlist = df_locations.values.tolist()

    map = folium.Map(
        location=[df_locations.latitude.mean(),
                  df_locations.longitude.mean()],
        zoom_start=15,
        zoom_control=34,
        control_scale=True,
        prefer_canvas=True
    )

    df.apply(plotDot, axis=1)
    for point in range(0, len(locationlist)):
        lat = df['latitude'][point]
        lon = df['longitude'][point]
        loc = lat, lon
        folium.Marker(locationlist[point], popup=loc).add_to(map)
    folium_static(map)

    # make the map wider
    make_map_responsive = """
        <style>
        [title ~= "st.iframe] { width: 100%}
        </style>
    """
    st.markdown(make_map_responsive,
                unsafe_allow_html=True)

    # text boxes to get user input
    lat = st.text_input("Latitude", "Type Here")
    long = st.text_input("Longitude", "Type Here")
    age = st.slider("Age", min_value=18, max_value=60, value=18)
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write(
        '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    attire = st.radio("Attire", ('Casual', 'Formal', 'Traditional'))
    pants = st.selectbox(
        'Pants Colour',
        ('Black', 'Blue', 'Blue Jeans', 'Grey', 'White', 'Brown', 'Red', 'Purple',
         'Orange', 'Pink', 'Yellow', 'Green'))
    time = st.slider("Time Spent (minutes)",
                     min_value=11, max_value=60, value=11)
    basket = st.selectbox(
        'Basket Colour',
        ('Black', 'Blue', 'Grey', 'White', 'Brown', 'Purple', 'Red',
         'Orange', 'Pink', 'Yellow', 'Green'))
    shirt = st.selectbox(
        'Shirt Colour',
        ('Black', 'Grey', 'White', 'Brown', 'Red',  'Blue', 'Purple',
         'Orange', 'Pink', 'Yellow', 'Green'))
    spent = st.slider("Total Spent (RM)", min_value=7, max_value=21, value=7)
    basket_size = st.radio("Basket Size", ('Big', 'Small'))
    result = ""

    # action to be taken if Predict button is clicked,
    if st.button("Predict"):
        # if option == 'Decision Tree':
        result = prediction(stack, lat, long, age, attire, pants,
                            time, basket, shirt, spent, basket_size)
        # else:
        #     result = prediction(lr,money,loan)
    # display classifier selected and the result
    st.success(' Bring Kids? {}'.format(result))


if __name__ == '__main__':
    main()
