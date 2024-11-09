# Public Transportation Ratings for Schools
 
## Introduction
A good education system is one of the most important aspects of a democracy for various reasons. It is also important to ensure that kids and teenagers can reach their school as easily as possible, for example with public transportation – especially lower income families often don’t have the resources to provide the transportation themselves. 
Of course, this is a very broad topic and has a lot of different aspects to be considered, e.g. a significant dependency on the discussed region. This portfolio focuses on analyzing the schools in Vienna and what their level of inclusion in the public transportation is.
Various biases and aspects not included in this portfolio are listed in the appendix.
## Background
Vienna is certainly one of the cities with the best public transportation systems in the world, as various studies suggest. While size (both population and area) can be assumed to contribute their parts to this fact, a lot of resources are dedicated by the city to provide a very reliable, very broad and efficient system (as some would say: “every trip takes around 30min”).
An assumption of myself is that the quality of public transportation system in Vienna leads to many people not having a car in the city (compared to other cities), which again leads to a certain dependency when it comes to schools – the city has to continuously provide reliable public transportation to the schools, as most people simple don’t have a car and can’t drive their kids to school, as it is more or less usual in other regions of Austria. Therefore, I decided to look at those connections and analyze how well schools are connected inside the city.

## Methodology
The methodology described below and the structure of it follows the 3 main components of an KGMS (which are also the basis for the Vadalog):
-	Neo4J as DMBS
-	Various notebooks to create and evolve the Graph itself 
-	Services and analytics separated from the step above, e.g. see the service in Figure 1.
  
The next subchapters describe the various aspects and parts implemented and assessed.
### Data
3 data resources have been used to create the knowledge graph:
-	A json-file containing all Stops (data.gv.at/wien_haltestellen) 
-	A json-file containg all public and private Schools (data.gv.at/schulenstandortewien)
-	A csv-file containing the transportation lines provided on a Stop (https://www.data.gv.at/katalog/dataset/36a8b9e9-909e-4605-a7ba-686ee3e1b8bf)
### Database
The Neo4J Graph Database was used for this project. On the one hand, it allows a quick and easy registration, allows more than enough free resources and instances, and can be easily connected with e.g. a Jupyter Notebook through the neomodel-library.
### Models
The models/entities used can be found under models.py:
-	Line: a specific Line, e.g. U6, containing name and type (metro, bus, nightbus, or tram)
-	Stop: a Stop, e.g. Absberggasse, containing (among other things) the coordinates and the derived relationship HAS_LINE to a Line
-	School: a public or private School, containing (amongst other things) the coordinates, and the derived relationships IS_NEARBY / IS_IN_AREA to a Stop if it is less than 300m / less than 600m away respectively. Furthermore, it contains a derived rating based on the number of different Lines nearby or in the area.
### Import and Evolution
Through the neomodel-library, one can easily connect a Neo4J instance and manipulate the Graph Database.
The notebook graph_creation.ipynb loads all 3 datasets into their respective model. While School and Stop were basically directly uploaded into the database, Line needed some processing. The provided data was only a list of departures of various lines from various stops, so there have been multiple duplicates on the one hand, and the relationship HAS_LINE from Stop to Line has also established at this point. In the same step, when a Line has been added, a type was analyzed based on the name: metro (‘U’ followed by single digit), bus (3 digits, or 1 or 2 digits followed by ‘A’ or ‘B’), tram (1 or 2 digits), or NA. City trains (“S-Bahn”) have been left out as a separate category, the reason behind it will be explained later.
The notebook graph_evolution.ipynb was responsible for calculating the Haversine Distance (great-circle distance between two points on a sphere) between all Schools and all Stops. This leads to the relationships IS_NEARBY (if less than 300m) and IS_IN_AREA (if more than 300m, but less than 600m). As one mostly cannot go directly from point A to point B in Vienna, this led to IS_NEARBY distances being a walk of around 450m and IS_IN_AREA distances a walk of around 750m, according to the 15 to 20 samples I took from Google Maps. The separation of distances of 300m/600m seem reasonable to me; for a 9-year-old, parents would probably prefer shorter walks, while for teenagers it is also okay to walk a little longer. The needs of both broadly described groups can be addressed with this logic.
The notebook graph_logical.ipynb is deriving the school-rating, in terms of “how well connected is a school in terms of public transportation”. The rating is derived by the following logic:
-	1, if at least one the following conditions meet:
o	4 or more lines + a metro nearby 300m
o	6 or more lines + a metro nearby 600m
o	8 or more lines nearby 600m
-	2, if at least one of the following conditions meet:
o	4 or more lines, none of them a metro, nearby 300m
o	6 or more lines, none of them a metro, nearby 600m
-	3, if at least one of the following conditions meet:
o	4 or more lines, none of them a metro, nearby 600m
o	A metro nearby 600m
-	4, if:
o	3 or more lines, none of them a metro, nearby 600m
-	5, if:
o	1 or 2 lines, none of them a metro, nearby 600m
-	6, if:
o	No lines nearby 600m
While the argument can be made that city trains (“S-Bahn”) provide a very fast transportation across the city, the reason for not including it separately lies in the definition of the city trains and the real-life application of this Graph – the assumption is made that children will go to schools nearby where they live, not at the other side of the city. One of the graph’s usages would be as a decision tool for parents on how well the schools of option are connected to public transportation are connected, including city trains separately should by the assumption above not have a significant impact as an own category.
## Real World Applications
As mentioned above, one of the real-world applications can be a decision tool for parents or legal guardians. When having a potential spot at 3 different schools, the parents/legal guardians can easily look up all nearby public transportations, which is especially of benefit if the kid would potentially drive from/to school to/from various locations (e.g., to grandparents or if the parents are divorced). An application for this usage has been implemented (search_good_schools.py). The basis for this service is Cypher-based querying and can therefore easily be extended to further address the information needs of the parents or legal guardian.
  
Furthermore, this Graph can be used as a tool for financial decisions of the city of Vienna. The city council can, through e.g. the mentioned service in Figure 1, analyze the connectedness for various schools to help deciding on future improvements, like with a higher clock rate or with new/extended lines. Other options as a decision-tool would be through querying the worst connected schools, or a deeper analysis of the “coverage” of those Line already provided (are 2 Lines of a school maybe both from south to west, not really including the north and east areas based on the schools location?).
### Comparing different data models
In the database community, knowledge graphs are primarily seen as a method for efficiently storing and querying interconnected data. The most common model here is the Labeled Property Graph, as implemented in Neo4j.
The semantic web community has a big focus on reasoning (SparQL) and data sharing (globally unique identifiers, URI’s). Query languages such as SparQL work with a subject-predicate-object kind of logic. While SparQL is higher expressive, it provides less performance compared to Label Property Graphs.
The machine learning community has a high emphasis on predictive insights which can be gained from a graph structure. This can be done for example through a Graph Neural Network or Graph Embeddings. While both examples are great for identifying structural similarities, they both don’t understand the semantics and lack interpretability capabilities.
The data science community views Knowledge Graphs from the perspective of exploratory analysis. Various cluster analyses or visualization techniques can be used for this approach.

## Results
The notebook graph-analytics.ipynb answers a few selected questions, which are listed in the subchapters below.
### What is the percentage of schools with rating of 2 or higher?
51%.
### Which schools have the highest number of nearby Lines nearby / in the area?
The “Volksschule der Erzdiözese Wien” and the “Gastgewerbefachschule des Schulvereins der Wiener Gastwirte“ both have 22 lines in the area. Those 2 schools are directly followed by two primary schools with 21 lines each. 
### Are there any schools which do not have any Line nearby 600m?
There are 4 such schools, all of them at the outer borders of the city:
-	'MS 22, Sonnenallee 116'
-	'VS Hannah-Arendt-Platz 8'
-	'VS 22, Sonnenallee 116'
-	'BgBRg Maria-Trapp-Platz 5'
### What's the average rating inside and outside of the first 9 districts?
The inner 9 districts have an average rating of 1.55, while the other districts have an average rating of 2.2. The spread widens if the third district, where at least parts of it are not that well connected outside of Rennweg and Landstraße, is not counted as an inner district. (To answer this question, a json-file including all vienna districts as polygons was downloaded)
Conclusion
When analyzing how well the schools are connected, there is a difference regarding location in inner or outer districts. In general, almost all schools do provide a connection nearby, more than half of them defined as good or very good by my own metrics. Further analytics can be done by defining a finer-grained classification of the various lines and the measurement of how well they are connected. A domain expert on this topic would be of great benefit.


#### How to run the notebooks
It is important to insert the own Neo4J credentials in the file credentials.py.
### Biases and Missing Data

1.	Dedicated school busses, which potentially exist especially on the borders of Vienna, are not included as I did not find any data for that
2.	The logial rules lead higher ratings towards the city center. However, if this is really a bias or just a matter of fact (as the city center and some other hotspots like Rennweg are just way better connected) can be discussed, I believe it is the latter one.
3.	Changing lines to get to school is not considered in this portfolio. This could be an issue for teenagers which shouldn’t have a problem with this; however, for a 9-year-old, I believe that parents try to not consider this option as they probably feel safer if the kids can directly drive to school and not have to switch the line e.g. on the Schottenring.
4.	Either the json-file for the Stops contains too much entries or the csv-file for the Stops to Lines is too short – there exist Stops with no line.
5.	Some of the School-data is outdated, for example the “Saudi Arabic Private School” is enlisted but closed in 2019.
