#RULE BASED CUSTOMER SEGMENTATION-GEZINOMI

#First, let's import the necessary libraries.
import pandas as pd

#Dataset was read.
df = pd.read_excel(r"gezinomi.xlsx")

#Let's get to know the dataset.
df.head()
df.columns
df.info()
df.nunique()
df.index
df["ConceptName"].value_counts()
df["SaleCityName"].value_counts()
df.groupby("SaleCityName")["Price"].sum()
df.groupby("ConceptName")["Price"].sum()
df.groupby("SaleCityName")["Price"].mean()
df.groupby("ConceptName")["Price"].mean()
df.groupby(["ConceptName","SaleCityName"])["Price"].mean()


# "SaleCheckInDayDiff" variable indicates how long before the Check-In date the customer made the purchase. I converted this variable to a categorical variable.
##First, let's get to know the "SaleCheckInDayDiff" variable.
df["SaleCheckInDayDiff"].value_counts()
df["SaleCheckInDayDiff"].min()
df["SaleCheckInDayDiff"].max()

## I divided the "SaleCheckInDayDiff" variable into intervals and named them.
bins = [-1,7,30,90,df["SaleCheckInDayDiff"].max()]
labels = ["LastMinuters","Potential Planners","Planners","Early Bookers"]
df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"], bins, labels=labels) #This statement categorizes the values in the SaleCheckInDayDiff column into intervals specified in the bins list. The labels list provides labels for each category. The category labels created as a result of this process are assigned to a new column named EB_Score.
df.head(50).to_excel("eb_scorew.xlsx", index=False) #This statement converts the data frame containing the first 50 rows selected to an Excel file named "eb_scorew.xlsx". The index=False parameter prevents adding the index column to the Excel file.

#I examined the average amount paid and the number of transactions in the city-concept-EB Score, city-concept-season, city-concept-CInDay breakdown.
df.groupby(["SaleCityName", "ConceptName", "EB_Score"]).agg({"Price": ["mean", "count"]})
df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})
df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})

#I sorted the output of the City-Concept-Season breakdown by Price.
agg_df = df.groupby(["SaleCityName","ConceptName","Seasons"]).agg({"Price":"mean"})
print(agg_df)

#I converted the names in the index to variable names.
agg_df.reset_index(inplace=True)
agg_df.head()

#I defined new level-based customers.
agg_df["sales_level_based"] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x), axis=1)
print(agg_df["sales_level_based"])

#I divided new customers (personas) into segments based on Price.
## Added segments to agg_df with the naming "SEGMENT".
## Described the segments.
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})


#I tried to classify new incoming customers and predict how much revenue they would bring.
##I sorted the resulting dataframe by the Price variable.
## For example, in which segment is "Antalya_Oda + Kahvaltı_High" and how much fee is expected?
agg_df.sort_values("Price")
new_user = "Antalya_Oda + Kahvaltı_High" #Instead of "Antalya_Oda + Kahvaltı_High", you can write the desired "sales_level_based" to get the result.
agg_df[agg_df["sales_level_based"] == new_user]

