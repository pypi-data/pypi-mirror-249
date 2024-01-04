from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import quantile_transform
from sklearn.decomposition import PCA
import numpy as np

def normalized_PCA(X, n_components=.8):
    X_pca = PCA(n_components=0.8).fit_transform(X.reshape(X.shape[0],-1))
    X_pca -= np.mean(X_pca, axis=0)
    X_pca /= np.std(X_pca, axis=0)
    
    return X_pca


# Maska co najmniej
def make_condition_map(n_cycles, n_concepts, factor, factor_range):
    # Factor must be the size of a problem
    # Decydujemy, ile chcemy uzyskać cyklów warunkowych i wytwarzamy
    # odpowiednią sinusoidę. Dalej normalizujemy ją przedziałowo i kwantyzujemy
    # do liczby koncepcji tak, aby można było ją wykorzystać jako zbiór indeksów
    # wartości warunku.
    condition_base = np.sin(np.linspace(0, np.pi*2*n_cycles, n_concepts))
    condition_base -= np.min(condition_base)
    condition_base /= np.max(condition_base)
    condition_base *= (n_concepts-1)
    condition_base = condition_base.astype(int)

    # Wprowadzamy progi warunków
    conditions = np.linspace(*factor_range, n_concepts)
    conditions_vals = conditions[condition_base]
    
    # Uzyskujemy mapę warunków przez przyrównanie dające nam macierz
    # Samples X concepts
    condition_map = factor[:,None] > conditions_vals[None,:]    
    
    return condition_map
   
def mix_to_factor(X, n_components=10, covtype='spherical'):
    # Modelujemy miksturę Gaussowską
    mixture = GaussianMixture(n_components=n_components,
                              covariance_type=covtype).fit(X)

    # Pobieramy i normalizujemy wsparcia
    # Dysponujemy macierzą mpp o wymiarach liczba obiektów x liczba centroidów
    # mikstury. Sumujemy więc po drugim wymiarze i kolejny raz normalizujemy
    mpp = mixture.predict_proba(X)
    print('mpps', mpp.shape)
    
    factor = quantile_transform(mpp,
                                output_distribution='uniform')
    factor = quantile_transform(np.sum(factor, axis=1).reshape(-1,1),
                                output_distribution='uniform').ravel()
    
    return factor
