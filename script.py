import pandas as pd
import numpy as np
from scipy.optimize import linprog
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder 
from sklearn.ensemble import RandomForestRegressor





def load_data(wk, folder):
    
    df1=pd.read_csv(os.path.join(folder, f"wk{wk}.csv"))
    df1['Cost']/=10

    try:
        df2=pd.read_csv(os.path.join(folder, f"wk{wk+1}.csv"))

        df2['Cost']/=10
        optimisation_df=df2[["Name", "Team", "Position", "Cost", "Points"]]

        return optimisation_df, df1


    except:
        return None, df1


def get_constraints(optimisation_df):
    BUDGET=80

    points=optimisation_df["Points"]
    cost=optimisation_df["Cost"]
    position=optimisation_df["Position"]
    name=optimisation_df["Name"]

    num=len(points)

    # Objective Function
    c=-np.array(points)

    clubs_le=LabelEncoder()
    clubs_le.fit(optimisation_df['Team'])
    clubs_encode=clubs_le.transform(optimisation_df['Team'])
    

    A_ub=[]
    A_ub.append(np.array(cost))
    for club_id in np.unique(clubs_encode):
        A_ub.append(np.array([1 if clubs_encode[i]==club_id else 0 for i in range(num)]))

    A_ub=np.array(A_ub)

    goalkeepers=np.array([1 if position[i]=='GKP' else 0 for i in range(num)])
    defenders=np.array([1 if position[i]=='DEF' else 0 for i in range(num)])
    midfielders=np.array([1 if position[i]=='MID' else 0 for i in range(num)])
    forwards=np.array([1 if position[i]=='FWD' else 0 for i in range(num)])

    A_eq=np.array([np.ones(num), goalkeepers, defenders, midfielders, forwards])

    b_ub=[BUDGET]+[3]*20
    b_eq=[15, 2, 5, 5, 3]


    return {
        "c":c,
        "A_ub":A_ub,
        "A_eq":A_eq,
        "b_ub":b_ub,
        "b_eq":b_eq,

        "points":points,
        "cost":cost,
        "clubs":clubs_encode,
        "name":name,
        "position":position,
        'teams':optimisation_df['Team'],
    }

def knapsack(constraints):
    
    points=constraints["points"]
    cost=constraints["cost"]
    clubs=constraints["clubs"]
    names=constraints["name"]
    position=constraints["position"]
    team=constraints["teams"]

    num=len(points)

    c=constraints["c"]
    A_ub=constraints["A_ub"]
    A_eq=constraints["A_eq"]
    b_ub=constraints["b_ub"]
    b_eq=constraints["b_eq"]

    integrality=np.full(num, 3)

    result=linprog(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,

        integrality=integrality,
        bounds=(0,1)
    )

    if result.success:
        return make_df(result, cost, points, names, position, team)

def make_df(result, cost, points, name, position, club):
   
    selected_cost, selected_points, selected_name, selected_position, selected_club=[],[],[],[],[]
    for i in range(len(result.x)):
        if result.x[i]!=0:
            selected_club.append(club[i])
            selected_cost.append(cost[i])
            selected_points.append(points[i])
            selected_name.append(name[i])
            selected_position.append(position[i])

    import pandas as pd
    df=pd.DataFrame({
        "Name":selected_name,
        "Team":selected_club,
        "Position":selected_position,
        "Points":selected_points,
        "Cost":selected_cost
    })

    df.sort_values(by=['Position', 'Points'], inplace=True, ascending=[True, False])

    return df.reset_index(drop=True),sum(df["Cost"]), sum(df["Points"])



class RandomF:
    def __init__(self, df) -> None:
        self.df=df


    def model_train(self):
        X=self.df.drop(["Name", "Bonus", "Points"], axis=1)
        y=self.df[["Points"]]

        ss=StandardScaler()
        ss.fit(X.iloc[:, 2:])
        X.iloc[:, 2:]=ss.transform(X.iloc[:, 2:])

        X["Team"]=LabelEncoder().fit_transform(X["Team"])
        X["Position"]=LabelEncoder().fit_transform(X["Position"])

        self.X=X
        self.y=y

        self.rfr=RandomForestRegressor(n_estimators=250, max_depth=13, max_features='sqrt', min_samples_leaf=2, min_samples_split=2, bootstrap=False)
        

        self.rfr.fit(self.X, self.y)

    def predict(self, train=False, *args):
        if train:
            X=self.X
        else:
            X=args
        
        
        self.preds=self.rfr.predict(X)

        return self.preds

    def metrics(self):
        from sklearn.metrics import mean_squared_error, r2_score
        try:
            return {"mse": mean_squared_error(self.y, self.preds), 
                "r2": r2_score(self.y, self.preds)}
        except:
            return "Please predict first"


            

def get_df(df, a, b, c):
    defenders=df.loc[df["Position"]=='DEF'][:a]
    goalkeepers=df.loc[df["Position"]=='GKP'][:1]
    midfielders=df.loc[df["Position"]=='MID'][:b]
    forwards=df.loc[df["Position"]=='FWD'][:c]

    df=pd.concat([goalkeepers, defenders, midfielders, forwards])

    return df
        




