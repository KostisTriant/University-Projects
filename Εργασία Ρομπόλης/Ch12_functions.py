{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "fd1e64f0",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'%.4f'"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import numpy as np                  \n",
    "import matplotlib.pyplot as plt\n",
    "import pandas as pd\n",
    "from scipy import stats\n",
    "%precision 4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "c97d6f21",
   "metadata": {},
   "outputs": [],
   "source": [
    "def BinTree(S,sigma,T,N):\n",
    "    \"\"\" Η συνάρτηση κατασκευάζει ένα διωνυμικό δέντρο.\n",
    "    -------------- ΠΑΡΑΜΕΤΡΟΙ------------------------\n",
    "    S: Η αρχική τιμή της μετοχής\n",
    "    sigma: Η μεταβλητότητα της μετοχής\n",
    "    T: Η διάρκεια του δέντρου\n",
    "    N: Ο αριθμός των περιόδων του δέντρου\n",
    "    \"\"\"\n",
    "    dt=T/N\n",
    "    u=np.exp(sigma*np.sqrt(dt))\n",
    "    d=1.0/u\n",
    "    tree=np.zeros((N+1,N+1))\n",
    "    for i in np.arange(N+1):\n",
    "        for j in np.arange(i+1):\n",
    "            tree[j,i]=S*u**j*d**(i-j)\n",
    "    return tree"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "63dba18d",
   "metadata": {},
   "outputs": [],
   "source": [
    "def BinTreeOption(S,K,T,r,q,sigma,N,flag1=\"call\",flag2=\"European\"):\n",
    "    \"\"\" Η συνάρτηση υπολογίζει την τιμή ενός Call or Put option\n",
    "    χρησιμοποιώντας ένα διωνυμικό δέντρο\n",
    "    -----------------------ΠΑΡΑΜΕΤΡΟΙ----------------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    K: τιμή εξάσκησης\n",
    "    Τ: διάρκεια μέχρι τη λήξη\n",
    "    r: επιτόκιο χωρίς κίνδυνο\n",
    "    q: μερισματική απόδοση μετοχής\n",
    "    sigma: Η μεταβλητότητα της μετοχής\n",
    "    N:  Ο αριθμός των περιόδων του δέντρου\n",
    "    flag1: \"call\" or \"put\", default value=\"call\"\n",
    "    flag2: \"European\" or \"American\", default value=\"European\"\n",
    "    \"\"\"\n",
    "    dt=T/N\n",
    "    u=np.exp(sigma*np.sqrt(dt))\n",
    "    d=1.0/u\n",
    "    prob=(np.exp((r-q)*dt)-d)/(u-d)\n",
    "    tree=BinTree(S,sigma,T,N)\n",
    "    treeT=tree[:,-1]\n",
    "    option_tree=np.zeros((N+1,N+1))\n",
    "    if flag2==\"European\":\n",
    "        if flag1==\"call\":\n",
    "            option_tree[:,-1]=np.maximum(treeT-K,0)\n",
    "        elif flag1==\"put\":\n",
    "            option_tree[:,-1]=np.maximum(K-treeT,0) \n",
    "        for i in reversed(np.arange(N)):\n",
    "            for j in np.arange(i+1):\n",
    "                option_tree[j,i]=np.exp(-r*dt)*((1-prob)*option_tree[j,i+1]+prob*option_tree[j+1,i+1])\n",
    "    elif flag2==\"American\":\n",
    "        if flag1==\"call\":\n",
    "            option_tree[:,-1]=np.maximum(treeT-K,0)\n",
    "        elif flag1==\"put\":\n",
    "            option_tree[:,-1]=np.maximum(K-treeT,0) \n",
    "        for i in reversed(np.arange(N)):\n",
    "            for j in np.arange(i+1):\n",
    "                if flag1==\"call\":\n",
    "                    intr_value=np.maximum(tree[j,i]-K,0)\n",
    "                    option_tree[j,i]=np.maximum(np.exp(-r*dt)*((1-prob)*option_tree[j,i+1]+prob*option_tree[j+1,i+1]),intr_value)\n",
    "                elif flag1==\"put\":\n",
    "                    intr_value=np.maximum(K-tree[j,i],0)\n",
    "                    option_tree[j,i]=np.maximum(np.exp(-r*dt)*((1-prob)*option_tree[j,i+1]+prob*option_tree[j+1,i+1]),intr_value)\n",
    "    return option_tree[0,0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "54c7d5f4",
   "metadata": {},
   "outputs": [],
   "source": [
    "def BSoptionprice(S,K,T,r,d,sigma,flag=\"call\"):\n",
    "    \"\"\" Η συνάρτηση υπολογίζει την τιμή ενός\n",
    "    Call or Put Option εφαρμόζοντας τους τύπους των Black-Scholes.\n",
    "    ------------------- ΠΑΡΑΜΕΤΡΟΙ -----------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    K: τιμή εξάσκησης\n",
    "    Τ: διάρκεια μέχρι τη λήξη\n",
    "    r: επιτόκιο χωρίς κίνδυνο\n",
    "    d: μερισματική απόδοση μετοχής\n",
    "    sigma: η μεταβλητότητα της μετοχής\n",
    "    flag: \"call\" or \"put\", default value=\"call\"\n",
    "    \"\"\"\n",
    "    d1 = (np.log(S/K)+(r-d+sigma**2/2)*T)/(sigma*np.sqrt(T))\n",
    "    d2 = d1 - sigma*np.sqrt(T)\n",
    "    if flag==\"call\":\n",
    "        P = S*np.exp(-d*T)*stats.norm.cdf(d1)-K*np.exp(-r*T)*stats.norm.cdf(d2)\n",
    "    elif flag==\"put\":\n",
    "        P=-S*np.exp(-d*T)*stats.norm.cdf(-d1)+K*np.exp(-r*T)*stats.norm.cdf(-d2)\n",
    "    return P"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "a8cace5a",
   "metadata": {},
   "outputs": [],
   "source": [
    "def BSGreeks(S,K,T,r,d,sigma):\n",
    "    \"\"\" Η συνάρτηση υπολογίζει τα Δέλτα, Γάμμα και Βέγκα των call and put options.\n",
    "    ------------------- ΠΑΡΑΜΕΤΡΟΙ -----------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    K: τιμή εξάσκησης\n",
    "    Τ: διάρκεια μέχρι τη λήξη\n",
    "    r: επιτόκιο χωρίς κίνδυνο\n",
    "    d: μερισματική απόδοση μετοχής\n",
    "    sigma: η μεταβλητότητα της μετοχής\n",
    "    \"\"\"\n",
    "    d1 = (np.log(S/K)+(r-d+sigma**2/2)*T)/(sigma*np.sqrt(T))\n",
    "    delta_call = np.exp(-d*T)*stats.norm.cdf(d1)\n",
    "    delta_put = -np.exp(-d*T)*stats.norm.cdf(-d1)\n",
    "    gamma = np.exp(-d*T)*stats.norm.pdf(d1)/(S*sigma*np.sqrt(T))\n",
    "    vega = S*np.exp(-d*T)*stats.norm.pdf(d1)*np.sqrt(T)\n",
    "    return (delta_call, delta_put, gamma, vega)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "abf67911",
   "metadata": {},
   "outputs": [],
   "source": [
    "def GBM(S,m,sigma,T,N):\n",
    "    \"\"\"Η συνάρτηση παράγει ένα τυχαίο μονοπάτι χρησιμοποιώντας τη προσομείωση Monte-Carlo με βάση τη Γεωμετρική Κίνηση Brown.\n",
    "    ---------------ΠΑΡΑΜΕΤΡΟΙ---------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    m: drift term\n",
    "    sigma: μεταβλητότητα της μετοχής\n",
    "    Τ: διάρκεια του μονοπατιού\n",
    "    Ν: αριθμός των βημάτων στο μονοπάτι\n",
    "    \"\"\"\n",
    "    dt=T/N\n",
    "    z = np.random.standard_normal(N) # δημιουργία τυχαίων αριθμών από την τυποποιημένη κανονική κατανομή\n",
    "    St = np.zeros(N)\n",
    "    St[0]=S\n",
    "    for j in np.arange(1,N):\n",
    "        St[j]=St[j-1]*np.exp((m-sigma**2/2)*dt+sigma*np.sqrt(dt)*z[j])\n",
    "    return St"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "f2111065",
   "metadata": {},
   "outputs": [],
   "source": [
    "def GBM(S,m,sigma,T,N):\n",
    "    \"\"\"Η συνάρτηση παράγει ένα τυχαίο μονοπάτι χρησιμοποιώντας τη προσομείωση Monte-Carlo με βάση τη Γεωμετρική Κίνηση Brown.\n",
    "    ---------------ΠΑΡΑΜΕΤΡΟΙ---------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    m: drift term\n",
    "    sigma: μεταβλητότητα της μετοχής\n",
    "    Τ: διάρκεια του μονοπατιού\n",
    "    Ν: αριθμός των βημάτων στο μονοπάτι\n",
    "    \"\"\"\n",
    "    dt=T/N\n",
    "    z = np.random.standard_normal(N) # δημιουργία τυχαίων αριθμών από την τυποποιημένη κανονική κατανομή\n",
    "    St = np.zeros(N)\n",
    "    St[0]=S\n",
    "    for j in np.arange(1,N):\n",
    "        St[j]=St[j-1]*np.exp((m-sigma**2/2)*dt+sigma*np.sqrt(dt)*z[j])\n",
    "    return St"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "5907522d",
   "metadata": {},
   "outputs": [],
   "source": [
    "def MCoptionprice(S,K,T,r,d,sigma,npaths,flag=\"call\",Antithetic=False):\n",
    "    \"\"\" Η συνάρτηση προσεγγίζει με προσομοίωση Monte Carlo \n",
    "    τις τιμές των Ευρωπαϊκών δικαιωμάτων για το υπόδειγμα των Black-Scholes. \n",
    "    ------------------- ΠΑΡΑΜΕΤΡΟΙ -----------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    K: τιμή εξάσκησης\n",
    "    Τ: διάρκεια μέχρι τη λήξη\n",
    "    r: επιτόκιο χωρίς κίνδυνο\n",
    "    d: μερισματική απόδοση μετοχής\n",
    "    sigma: η μεταβλητότητα της μετοχής\n",
    "    npaths: αριθμός προσομοιώσεων\n",
    "    flag: \"call\" or \"put\", default value=\"call\"\n",
    "    Antithetic: use Antithetic variates technique, default value=False\n",
    "    \"\"\"\n",
    "    zin = np.random.standard_normal(npaths)               # δημιουργία τυχαίων αριθμών από την τυποποιημένη κανονική κατανομή\n",
    "    if Antithetic:\n",
    "        z = np.array([zin,-zin]).flatten()\n",
    "        z = stats.zscore(z)\n",
    "    else:\n",
    "        z=zin\n",
    "    ST=S*np.exp((r-d-sigma**2/2)*T+sigma*np.sqrt(T)*z)    # υπολογισμός της τιμής της μετοχής στη λήξη\n",
    "    if flag==\"call\":\n",
    "        payoffs = np.maximum(ST-K, 0)\n",
    "    elif flag==\"put\":\n",
    "        payoffs = np.maximum(K-ST, 0)                     \n",
    "    option_price = np.mean(payoffs)*np.exp(-r*T)\n",
    "    option_analyt = BSoptionprice(S,K,T,r,d,sigma,flag)   # υπολογισμός της τιμής του option αναλυτικά με βάση το υπόδειγμα BS \n",
    "    error = option_analyt - option_price                  # υπολογισμός του σφάλματος αποτίμησης μέσω προσομείωσης\n",
    "    return (option_price, error)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "17b207ab",
   "metadata": {},
   "outputs": [],
   "source": [
    "def MC_call_put_Greeks(S,K,T,r,d,sigma,npaths):\n",
    "    \"\"\" Η συνάρτηση υπολογίζει μέσω προσομοίωσης Monte Carlo\n",
    "    τις ευαισθησίες των δικαιωμάτων.\n",
    "    ------------------- ΠΑΡΑΜΕΤΡΟΙ -----------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    K: τιμή εξάσκησης\n",
    "    Τ: διάρκεια μέχρι τη λήξη\n",
    "    r: επιτόκιο χωρίς κίνδυνο\n",
    "    d: μερισματική απόδοση μετοχής\n",
    "    sigma: η μεταβλητότητα της μετοχής\n",
    "    npaths: αριθμός προσομοιώσεων\n",
    "    \"\"\"\n",
    "    # υπολογισμός αρχικής τιμής δικαιωμάτων στο επίπεδο της τιμής S\n",
    "    (call_0,error_call) = MCoptionprice(S,K,T,r,d,sigma,npaths,\"call\",True)\n",
    "    (put_0,error_put) = MCoptionprice(S,K,T,r,d,sigma,npaths,\"put\",True)\n",
    "    \n",
    "    dS = S/100                                                   # μεταβολή της τιμ΄ής 1%\n",
    "    \n",
    "    dvol = sigma/100                                             # μεταβολή της μεταβλητότητας 1%\n",
    "    \n",
    "    # ευαισθησία σε μικρές μεταβολές της τιμής - Δέλτα και Γάμμα\n",
    "    (call_up, error_call_up) = MCoptionprice(S+dS,K,T,r,d,sigma,npaths,\"call\",True) # τιμή των call option στο S+dS\n",
    "    (call_dn, error_call_dn) = MCoptionprice(S-dS,K,T,r,d,sigma,npaths,\"call\",True) # τιμή των call option στο S-dS\n",
    "    (put_up, error_put_up) = MCoptionprice(S+dS,K,T,r,d,sigma,npaths,\"put\",True) # τιμή των put option στο S+dS\n",
    "    (put_dn, error_put_dn) = MCoptionprice(S-dS,K,T,r,d,sigma,npaths,\"put\",True) # τιμή των put option στο S-dS\n",
    "    \n",
    "    delta_call_up = (call_up-call_0)/dS                           # Δέλτα call στην άνοδο της τιμ΄ής +1%\n",
    "    \n",
    "    delta_call_dn = (call_dn-call_0)/(-dS)                        # Δέλτα call στην πτώση της τιμ΄ής -1%\n",
    "    \n",
    "    delta_call = (delta_call_up + delta_call_dn)/2                # υπολογισμός του Δέλτα call - μέση τιμή στα 2 σενάρια\n",
    "    \n",
    "    delta_put_up = (put_up-put_0)/dS                              # Δέλτα put στην άνοδο της τιμ΄ής +1%\n",
    "\n",
    "    delta_put_dn = (put_dn-put_0)/(-dS)                           # Δέλτα put στην πτώση της τιμ΄ής -1%            \n",
    "    \n",
    "    delta_put = (delta_put_up + delta_put_dn)/2                   # υπολογισμός του Δέλτα put - μέση τιμή στα 2 σενάρια     \n",
    "    \n",
    "    gamma_call = (delta_call_up - delta_call_dn)/dS               # υπολογισμός του γάμμα call \n",
    "    gamma_put = (delta_put_up - delta_put_dn)/dS                  # υπολογισμός του γάμμα put\n",
    "    gamma = (gamma_call + gamma_put)/2                            # Γάμμα call/put - μέση τιμή γάμμα call και γάμμα put\n",
    "    \n",
    "    # ευαισθησία σε μικρές μεταβολές της μεταβλητότητας - Βέγκα\n",
    "    (call_up, error_call_up) = MCoptionprice(S,K,T,r,d,sigma+dvol,npaths,\"call\",True) # τιμή των call option στο vol+dvol\n",
    "    (call_dn,error_call_dn) = MCoptionprice(S,K,T,r,d,sigma-dvol,npaths,\"call\",True) # τιμή των call option στο vol-dvol\n",
    "    (put_up, error_put_up) = MCoptionprice(S,K,T,r,d,sigma+dvol,npaths,\"put\",True) # τιμή των put option στο vol+dvol\n",
    "    (put_dn,error_put_dn) = MCoptionprice(S,K,T,r,d,sigma-dvol,npaths,\"put\",True) # τιμή των put option στο vol-dvol\n",
    "    \n",
    "    vega_call_up = (call_up-call_0)/dvol                            # Βέγκα call στην περίπτωση ανόδου\n",
    "    vega_call_dn = (call_dn-call_0)/(-dvol)                         # Βέγκα call στην περίπτωση καθόδου\n",
    "    vega_call = (vega_call_up + vega_call_dn)/2                     # Βέγκα call - μέση τιμή στα 2 σενάρια\n",
    "    \n",
    "    vega_put_up = (put_up-put_0)/dvol                               # Βέγκα put στην περίπτωση ανόδου           \n",
    "    vega_put_dn = (put_dn-put_0)/(-dvol)                            # Βέγκα put στην περίπτωση καθόδου\n",
    "    vega_put = (vega_put_up + vega_put_dn)/2                        # Βέγκα put - μέση τιμή στα 2 σενάρια\n",
    "    \n",
    "    vega = (vega_call + vega_put)/2                                 # Βέγκα call/put - μέση τιμή vega call και vega put\n",
    "    \n",
    "    return (delta_call, delta_put, gamma, vega)                     # επιστρέφει τις ευαισθησίες των δικαιωμάτων"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "8673f306",
   "metadata": {},
   "outputs": [],
   "source": [
    "def MC_Asian(S,K,T1,T2,r,d,sigma,N,npaths,flag=\"call\"):\n",
    "    \"\"\" Η συνάρτηση υπολογίζει με Monte Carlo προσομοίωση\n",
    "    τις τιμές των Ασιατικών Δικαιωμάτων προαίρεσης\n",
    "    ------------------- ΠΑΡΑΜΕΤΡΟΙ -----------------------\n",
    "    S: τρέχουσα τιμή της μετοχής\n",
    "    K: τιμή εξάσκησης\n",
    "    Τ1: διάρκεια μέχρι τη λήξη του δικαιώματος\n",
    "    Τ2: διάρκεια μέχρι την αρχή της περιόδου υπολογισμού του αριθμητικού μέσου (Τ2 < Τ1)\n",
    "    r: επιτόκιο χωρίς κίνδυνο\n",
    "    d: μερισματική απόδοση μετοχής\n",
    "    sigma: η μεταβλητότητα της μετοχής\n",
    "    N: αριθμός των βημάτων σε κάθε μονοπάτι\n",
    "    npaths: αριθμός προσομοιώσεων\n",
    "    flag: \"call\" or \"put\", default value=\"call\" \n",
    "    \"\"\"\n",
    "    dt=T1/N\n",
    "    N_in=int(T2//dt)\n",
    "    nsteps=N-N_in\n",
    "    Spath=np.zeros((2*npaths,nsteps))\n",
    "    zin = np.random.standard_normal((npaths,nsteps))\n",
    "    z = np.vstack((zin,-zin)) # use Anthithetic variates\n",
    "    z = stats.zscore(z)\n",
    "    Spath[:,0]=S*np.exp((r-d-sigma**2/2)*T2+sigma*np.sqrt(T2)*z[:,0])\n",
    "    for j in np.arange(1,nsteps):\n",
    "        Spath[:,j]=Spath[:,j-1]*np.exp((r-d-sigma**2/2)*dt+sigma*np.sqrt(dt)*z[:,j])\n",
    "    S_avg=Spath.mean(axis=1)\n",
    "    if flag==\"call\":\n",
    "        payoff=np.maximum(S_avg-K,0)\n",
    "    elif flag==\"put\":\n",
    "        payoff=np.maximum(K-S_avg,0)\n",
    "    option_price=np.exp(-r*T1)*np.mean(payoff)\n",
    "    return option_price"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "feef8fd6",
   "metadata": {},
   "outputs": [],
   "source": [
    "def MC_Asian_call_put_Greeks(S,K,T1,T2,r,d,sigma,N,npaths):\n",
    "    \"\"\" Η συνάρτηση υπολογίζει μέσω Monte Carlo προσομοίωσης\n",
    "    τις ευαισθησίες Ασιατικών Δικαιωμάτων Προαίρεσης \"\"\"\n",
    "    \n",
    "    # υπολογισμός αρχικής τιμής δικαιωμάτων στο επίπεδο τιμής S\n",
    "    call_0=MC_Asian(S,K,T1,T2,r,d,sigma,N,npaths)\n",
    "    put_0=MC_Asian(S,K,T1,T2,r,d,sigma,N,npaths,\"put\")\n",
    "    \n",
    "    dS = S/100                                          # μεταβολή της τιμ΄ής 1%\n",
    "    dvol = sigma/100                                    # μεταβολή της μεταβλητότητας 1%\n",
    "    \n",
    "    # ευαισθησία σε μικρές μεταβολές της τιμής - Δέλτα και Γάμμα\n",
    "    call_up=MC_Asian(S+dS,K,T1,T2,r,d,sigma,N,npaths) # τιμή των call options στο S+dS\n",
    "    call_dn=MC_Asian(S-dS,K,T1,T2,r,d,sigma,N,npaths) # τιμή των call options στο S-dS \n",
    "    \n",
    "    put_up=MC_Asian(S+dS,K,T1,T2,r,d,sigma,N,npaths,\"put\") # τιμή των put options στο S+dS\n",
    "    put_dn=MC_Asian(S-dS,K,T1,T2,r,d,sigma,N,npaths,\"put\") # τιμή των put options στο S-dS \n",
    "    \n",
    "    delta_call_up = (call_up-call_0)/dS                 # Δέλτα call στην άνοδο της τιμ΄ής +1%          \n",
    "    delta_call_dn = (call_dn-call_0)/(-dS)              # Δέλτα call στην πτώση της τιμ΄ής -1%          \n",
    "    delta_call = (delta_call_up + delta_call_dn)/2      # υπολογισμός του Δέλτα call - μέση τιμή στα 2 σενάρια\n",
    "    \n",
    "    delta_put_up = (put_up-put_0)/dS                    # Δέλτα put στην άνοδο της τιμ΄ής +1%\n",
    "    delta_put_dn = (put_dn-put_0)/(-dS)                 # Δέλτα put στην πτώση της τιμ΄ής -1%\n",
    "    delta_put = (delta_put_up + delta_put_dn)/2         # υπολογισμός του Δέλτα put - μέση τιμή στα 2 σενάρια\n",
    "    \n",
    "    gamma_call = (delta_call_up - delta_call_dn)/dS     # υπολογισμός του γάμμα call \n",
    "    gamma_put = (delta_put_up - delta_put_dn)/dS        # υπολογισμός του γάμμα put\n",
    "    gamma = (gamma_call + gamma_put)/2                  # Γάμμα call/put - μέση τιμή γάμμα call και γάμμα put\n",
    "    \n",
    "    # ευαισθησία σε μικρές μεταβολές της μεταβλητότητας - Βέγκα\n",
    "    call_up=MC_Asian(S,K,T1,T2,r,d,sigma+dvol,N,npaths)   # τιμή των call options στο vol+dvol\n",
    "    call_dn=MC_Asian(S,K,T1,T2,r,d,sigma-dvol,N,npaths)   # τιμή των call options στο vol-dvol\n",
    "    \n",
    "    put_up=MC_Asian(S,K,T1,T2,r,d,sigma+dvol,N,npaths,\"put\")   # τιμή των put options στο vol+dvol\n",
    "    put_dn=MC_Asian(S,K,T1,T2,r,d,sigma-dvol,N,npaths,\"put\")   # τιμή των put options στο vol-dvol\n",
    "    \n",
    "    vega_call_up = (call_up-call_0)/dvol                # Βέγκα call στην περίπτωση ανόδου\n",
    "    vega_call_dn = (call_dn-call_0)/(-dvol)             # Βέγκα call στην περίπτωση καθόδου\n",
    "    vega_call = (vega_call_up + vega_call_dn)/2         # Βέγκα call - μέση τιμή στα 2 σενάρια\n",
    "\n",
    "    vega_put_up = (put_up-put_0)/dvol                   # Βέγκα put στην περίπτωση ανόδου\n",
    "    vega_put_dn = (put_dn-put_0)/(-dvol)                # Βέγκα put στην περίπτωση καθόδου\n",
    "    vega_put = (vega_put_up + vega_put_dn)/2            # Βέγκα put - μέση τιμή στα 2 σενάρια\n",
    "    vega = (vega_call + vega_put)/2                     # Βέγκα call/put - μέση τιμή vega call και vega put\n",
    "\n",
    "    return (delta_call, delta_put, gamma, vega)         # επιστρέφει τις ευαισθησίες των δικαιωμάτων"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
