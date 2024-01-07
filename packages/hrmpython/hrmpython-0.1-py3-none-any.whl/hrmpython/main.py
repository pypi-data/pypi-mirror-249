import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

class HRM():
    """
    A class for handling High Resolution Melting (HRM) analysis on genetic data.
    """

    def __init__(self, df):
        """
        Initialize HRM object with a DataFrame containing temperature and fluorescence intensity.

        Parameters:
        - df: DataFrame, input data with temperature in the first column and fluorescence intensity in the rest.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a DataFrame.")

        # Check if the first column is named 'Temperature'
        if df.columns[0] != 'Temperature':
            raise ValueError("The first column must be named 'Temperature'.")

        # Check if the 'Temperature' column contains only float numbers
        if not pd.api.types.is_float_dtype(df['Temperature']):
            raise ValueError("The 'Temperature' column must contain only float numbers.")

        # Check if the DataFrame is valid (e.g., has the necessary columns)
        if df.shape[1] < 2:
            raise ValueError("DataFrame must have at least two columns (including 'Temperature').")
        
        # Assign the DataFrame to the object
        self.df = df
        self.temp = self.df.iloc[:, 0]
        self.data = self.df.iloc[:, 1:]
        self.clustering('kmeans', 2)

    def subset(self, _range):
        """
        Subset the data based on a temperature range.

        Parameters:
        - _range: tuple, temperature range to subset the data.

        Updates the 'temp' and 'data' attributes with the subsetted data.
        """
        df = self.df
        df = df[(df.iloc[:, 0] > _range[0]) & (df.iloc[:, 0] < _range[1])]
        self.temp = df.iloc[:, 0]
        self.data = df.iloc[:, 1:]

    def normal(self):
        """
        Normalize fluorescence intensity to a 0-100 scale.

        Returns:
        - DataFrame, normalized fluorescence intensity.
        """
        data = self.data
        return (data - data.min()) / (data.max() - data.min()) * 100

    def diff(self):
        """
        Calculate the differences between consecutive normalized data points.

        Returns:
        - DataFrame, differences between consecutive normalized data points.
        """
        data = self.normal()*-1
        return data.diff()
    
    def tm(self):
        """
        Calculate melting temperature (Tm) for each sample.

        Args:
        - df (DataFrame): Input DataFrame with 'temperature' column and sample columns.

        Returns:
        - DataFrame: A new DataFrame with the melting temperature for each sample.
        """
        df = pd.concat([self.temp, self.diff()], axis=1)
        tm = df.set_index('Temperature').idxmax()
        tm = tm.reset_index()
        tm.columns = ['Sample', 'Temperature']
        return tm 

    def sub(self, ref):
        """
        Subtract a reference sample from all samples in the normalized data.

        Parameters:
        - ref: str, the reference sample to subtract.

        Returns:
        - DataFrame, subtracted normalized data.
        """
        data = self.normal()
        return data.sub(data[ref], axis=0)

    def clustering(self, method, n):
        """
        Perform clustering on the transposed normalized data.

        Parameters:
        - data: DataFrame, fluorescence intensity.
        - method: str, clustering method ('kmeans', 'agglomerative', or 'dbscan').
        - n: int, number of clusters.

        Returns:
        - ndarray, cluster labels for each sample.
        """
        data = self.normal()
        if method == 'kmeans':
            kmeans = KMeans(n_clusters=n)
            self.cluster = kmeans.fit_predict(data.T)
        elif method == 'agglomerative':
            agglomerative = AgglomerativeClustering(n_clusters=n)
            self.cluster = agglomerative.fit_predict(data.T)
        elif method == 'dbscan':
            dbscan = DBSCAN(eps=0.2)
            self.cluster = dbscan.fit_predict(data.T)

    def reshape(self, data):
        """
        Reshape the data for visualization, adding cluster information.

        Parameters:
        - data: DataFrame, fluorescence intensity.
        - cluster: ndarray, cluster labels for each sample.

        Returns:
        - DataFrame, reshaped data for visualization.
        """
        df = pd.concat([self.temp, data], axis=1)
        tmp = []
        for i in range(len(data.columns)):
            melt = pd.melt(df.iloc[:, [0, i + 1]], id_vars=['Temperature'], var_name='Sample', value_name='Intensity')
            if self.cluster is not None:
                melt['Cluster'] = self.cluster[i]
            tmp.append(melt)
        return pd.concat(tmp, ignore_index=True)