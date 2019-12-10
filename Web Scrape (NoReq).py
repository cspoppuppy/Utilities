from bs4 import BeautifulSoup
import pandas as pd

# Get attributes into each category
def GetCustomerAttributes(l):
    user_cases=[]
    industry=[]
    location=[]
    products=[]
    for i in l:
        # User Case
        if i[0:23]=="data-use_cases_applied-":
            user_cases.append(i.replace("data-use_cases_applied-",""))
        # Industry
        elif i[0:25]=="data-industry_categories-":
            industry.append(i.replace("data-industry_categories-",""))
        # Location
        elif i[0:21]=="data-location_region-":
            location.append(i.replace("data-location_region-",""))
        # Products
        elif i[0:19]=="data-products_used-":
            products.append(i.replace("data-products_used-",""))
    return [user_cases, industry, location, products]

def MergeDfs(l,key):
    df=l[0]
    for i in l[1:]:
        df=pd.merge(df, i, left_on=key, right_on=key)
    return df


if __name__=="__main__":
    # Copied webpage html in a text file in advance
    # Request to the specific website (Twilio) takes too long (after modify browser user agent, the site not support web scrape)
    with open ("customers.txt","r") as f:
        data=f.read()

    # Find relevant tags
    # Customer name, URL and attribution under uk-width-medium-1-3 grid-item
    # Headlines under list-item-headline
    # Detailed description under grid-item-content
    soup=BeautifulSoup(data, features='html.parser')
    div1=soup.findAll('div',{'class':'uk-width-medium-1-3 grid-item'})
    ##info=soup.select('[class~=grid-item__story-link]')
    div2=soup.findAll('div',{'class':'list-item-headline'})
    div3=soup.findAll('div',{'class':'grid-item-content'})

    # Search under tag uk-width-medium-1-3 grid-item (copied to div1)
    index=[]
    cust=[]
    cust_url=[]
    cust_attr=[]
    l=[]
    attr_usercase=[]
    attr_industry=[]
    attr_location=[]
    attr_products=[]
    for idx, d in enumerate(div1):
        index.append(idx+1)
        cust.append(d.find('a')['href'].rsplit('/',1)[-1])
        cust_url.append(d.find('a')['href'])
        cust_attr.append(d.attrs)
        # Attribution
        l=GetCustomerAttributes(list(d.attrs.keys()))
        attr_usercase.append(", ".join(l[0]))
        attr_industry.append(", ".join(l[1]))
        attr_location.append(", ".join(l[2]))
        attr_products.append(", ".join(l[3]))
    # Output results to dataframe
    df_custDetails=pd.DataFrame({"Id":index, "Customer":cust, "URL":cust_url, "Attributes":cust_attr, "User Case": attr_usercase, "Industry":attr_industry, "Location": attr_location, "Products": attr_products})
    print("Customer Details...")
    print(df_custDetails)

    # Search under tag list-item-headline (copied to div2)
    index=[]
    headline=[]
    for idx, d in enumerate(div2):
        index.append(idx+1)
        headline.append(d.text.replace("\n",""))
    # Output results to dataframe
    df_CustHeadline=pd.DataFrame({"Id":index, "Headline":headline})
    print("Customer Headline...")
    print(df_CustHeadline)

    # Search under tag grid-item-content (copied to div3)
    index=[]
    desc=[]
    for idx, d in enumerate(div3):
        index.append(idx+1)
        desc.append(d.text.replace("\n",""))
    # Output results to dataframe
    df_CustDesc=pd.DataFrame({"Id":index, "Description":desc})
    print("Customer Description...")
    print(df_CustDesc)

    # Combine results
    df=MergeDfs([df_custDetails, df_CustHeadline, df_CustDesc], "Id")
    print("Combined results...")
    print(df)
    df.to_csv("Customer.csv")

