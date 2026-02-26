from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


model = load_model('microp-app-be\prediction_microplastic.h5')


coastline_gdf = gpd.read_file('microp-app-be\\ne_10m_coastline.shp')
ocean = gpd.read_file('microp-app-be\\ne_10m_ocean.shp')

df=pd.read_csv("microp-app-be\output_file_with_distance.csv")
df=df.drop(columns="Country_code")

X=df.drop(columns="Measurement")
y=df["Measurement"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

def find_distance(lat,lon,coastline_gdf):
    point = Point(lon, lat)

    # Calculate the distance to the nearest land using the distance method
    distance_to_nearest_land = coastline_gdf.distance(point).min()

    return distance_to_nearest_land

def get_microplastic_prediction(lat,lon,X_train=X_train):
    Latitude=lat
    Longitude=lon 
    Distance=find_distance(Latitude,Longitude,coastline_gdf)
    Population=1428627663
    print(Longitude)
    
    

    def is_in_ocean(latitude, longitude):
        point = Point(longitude, latitude)
        for index, row in ocean.iterrows():
            if point.within(row['geometry']):
                return True  # Clicked coordinates are in the ocean
        return False  # Clicked coordinates are not in the ocean


    if is_in_ocean(Latitude, Longitude):
        print("The clicked coordinates are in the ocean.")
    else:
        print("The clicked coordinates are not in the ocean.")
        return "Not found"


    new_data_point={
    "Latitude":Latitude, "Longitude":Longitude,"Population":Population,"Distance_From_Land":Distance
    }

    new_data_point = pd.DataFrame([new_data_point])

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    new_data_point_scaled = scaler.transform(new_data_point)
    predicted_value = model.predict(new_data_point_scaled)
    return predicted_value[0][0]

print(get_microplastic_prediction(13.049958, 80.347480))





