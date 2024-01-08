# Desctiption of models 

For all models:

- $x_c$: [mm] carbonation depth
- $t$: [years] time

## CECS 220-2007 (2007)

The model of the chinese "Standard for durability assessment of concrete structures" [CECS 220-2007](https://www.chinesestandard.net/PDF/English.aspx/CECS220-2007) takes several factors influencing the carbonation of concrete into account. 
In addition to humidity, temperature, and $CO_2$ content it also distinguishes between pressure and tension conditions of the component. 
The compressive strength, the amount of fly ash in the cement and if the carbonation depth is calculated for a corner of the component or another area are also taken into account. 
The carbonation depth $x_c(t)$ [mm] is described as follows:



$$x_c(t)=3 \cdot K_{CO_2}\cdot K_{kl}\cdot K_{kt}\cdot K_{ks}\cdot K_F\cdot T^{0.25}RH^{1.5}(1-RH)\Bigl(\frac{58}{f_{cuk}}-0.76\Bigr)\cdot\sqrt{t}$$

$t$: time [years]

$K_{CO_2}$: $CO_2$ density factor: [-] 

- $K_{CO_2}=\sqrt{\frac{c_{Co_2}}{0.03}}$ 

-  $c_{CO_2}$: $CO_2$ concentration [\%] 

$K_{kl}$: location factor: [-]

| Location  | $K_{kl} $     |
|-----------|---------------|
| corner of the component    | 1.4 |
| other areas      | 1.0|


$K_{kt}$: curing factor: [-] $K_{kt}=1.2$ 

$K_{ks}$: stress factor: [-]

| Condition             | $K_{ks}$  |
|-----------------------|-----------|
| Compression condition | $1.0$     |
| Tension condition     | $1.1$     |


$K_{F}$: fly ash factor: [-]

- $K_F=1.0+13.34\cdot F^{3.3}$ 

- $F$: fly ash content [weight ratio] 

$T$: annual temperature [°C] 

$RH$: annual relative humidity [-] 

$f_{cuk}$: charasteristic strength [MPa]


**Note:** The CECS 220-2007 model is described by [Sun et al.](https://www.sciencedirect.com/science/article/pii/S0141029619332754) 



| Variable Name | Doc                                                   | Unit   | One_of                         | GUI Key                   |
|---------------|-------------------------------------------------------|--------|--------------------------------|---------------------------|
| f_c           | concrete characteristic compressive strength        | MPa   |                                | Compressive Strength     |
| FA_c          | fly ash content                                      | count  |                                | Fly Ash Content         |
| stress        | stress on component                                  |        | tension, pressure              | Stress                    |
| location      | location of component                                |        | corner, other area             | Location                  |
| T             | temperature                                          | °C     |                                | Temperature               |
| RH            | relative humidity around concrete surface            | %      |                                | Relative Humidity         |
| CO2           | CO2 density around concrete surface                  | %      |                                | CO2 Concentration        |



## Ekolu (2018)
The model of [Ekolu](https://www.sciencedirect.com/science/article/pii/S0958946516307570) \cite{Ekolu.2018} was created from existing mathematical formulas whose parameters were adjusted through a 10-year study. 
In this experimental study, different specimens of concrete with different cement compositions, compressive strengths, water-cement ratios, and three different curing methods or conditions were prepared and then stored externally for several years. After 3.5, 6 and 10 years, the compressive strength as well as the carbonation depth were measured from each of the specimens.  
The Ekolu model has some **limitations**:
 - the relative humidity must be between 50 and 80 %
 - the compressive strength must exceed 20 MPa
 - the model cannot be used for indoor components. 
 
The carbonatiion depth $x_c(t)$ [mm] is calculated as:

$$x_c(t)=e_h \cdot e_s\cdot e_{co}\cdot cem \cdot \bigl(F_{c(t)}\bigr)^g\cdot \sqrt{t}$$


$t$: [years]  time

$cem$: [-]  factor from table in dependence of binder type

$g$: [-]  factor from table in dependence of binder type
- **Note:** In App implemented with *Cement types*

| SCM | Cement types     | $cem$ [-] | $g$ [-]  |
|-----------------------|---------------------|---------:|--------:|
| 20\% Any              | CEM I, CEM II/A     |     1000 |    -1,5 |
| 30\% Fly ash          | CEM II/B, CEM IV/A |     1000 |    -1,4 |
| 50\% Slag             | CEM III/A, CEM IV/B|     1000 |    -1,4 |


$e_h$: environmental factor for relative humidity 
- **Note:** defined for 50 $\leq$ RH $\leq$ 80 %:
$$e_h=16\Bigl(\frac{RH-35}{100}\Bigr)\Bigl(1-\frac{RH}{100}\Bigr)^{1.5} $$ 
- $RH$: [\%] relative humidity 

$e_s$: [-] environmental factor for shelter 
- $f_{c28}$: 28-day compressive strength [MPa]

| Exposure             | $e_s$                                     |
|----------------------|-------------------------------------------|
| Outdoor, protected from rain   | $e_s=1,0$ |
| Outdoor, exposed to rain      | $e_s=f_{c,28}^{-0.2}$|


$e_{co}$: environmental factor for varied $CO_2$ concentrations


|   $f_{c,28}$        | $e_{co}$                                     |
|----------------------|-------------------------------------------|
| for $20 < f_{c,28} < 60$ MPa   | $e_{co}=\alpha \cdot f_{c,28}^r$  |
| for $f_{c,28}\geq60$ MPa  | $e_{co}=1.0$ |

- with $\alpha$ and $r$ in dependence of $CO_2$:

   |  $CO_2$      |  200 ppm  |  300 ppm  |  500 ppm  | 1000 ppm  | 2000 ppm  |
   |--------|----------|----------|----------|----------|----------|
   | $\alpha$ [-] |        1.4 |        1.0 |        2.5 |        4.5 |        14 |
   | $r$ [-]     |      -1/4 |          0 |      -1/4 |      -2/5 |      -2/3 |


$g$: conductance factor [-] 
$cem$: scalar 

$F_{c(t)}$: time-dependent strenght growth function 
$$F_{c(t)}=\frac{t}{a+b\cdot t}\cdot f_c$$

- $f_c$: strength (28-day compressive strenght or long-term (field) strenght) 
- $a$, $b$: constants: 

   |$f_c$ from |$t$ [years]|$a$|$b$|
   |-------------|----|---|---|
   | 28-day strenght  $f_c=f_{c28}$| $t<6$ | $0.35$| $0.6-\frac{t^{0.5}}{50}$ |
   |  28-day strenght $f_c=f_{c28}$| $t\geq6$|$0.15 \cdot t$| $0.5-\frac{t^{0.5}}{50}$ |
   |long-term (field) strenght $f_c=f_{cbn}$|$t<15$ |$0.35$| $1.15-\frac{t^{0.6}}{50}$ |
   |long-term (field) strenght $f_c=f_{cbn}$|$t\geq15$|$0.15 \cdot t$| $0.95-\frac{t^{0.6}}{50}$|

   - **Note:** In the App only $f_c=f_{c28}$ is implemented.

| Variable Name | Doc                                                               | Unit  | GUI Key             | One Of                              | Min Value | Max Value |
|---------------|-------------------------------------------------------------------|-------|---------------------|-------------------------------------|-----------|-----------|
| f_c           | 28-day compressive strength (NOT:long-term (field) strength)    | MPa  | Compressive Strength|                                     | 20        |           |
| RH            | relative humidity                                                 | %     | Relative Humidity   |                                     | 50        | 80        |
| CEM           | cement type                                                       |       | Cement Type         | CEM I, CEM II/A, CEM II/B, CEM IV/A, CEM III/A, CEM IV/B |           |           |
| ExCo          | exposure conditions                                               |       | Exposure Condition  | Exposed, Sheltered                  |           |           |
| CO2           | peripheral concentration by weight of CO2                        | %     | CO2 Concentration   |                                     |           |           |



## fib Model Code Service Life Design (2006)

In [fib Model Code Service Life Design (2006)](https://www.fib-international.org/publications/fib-bulletins/model-code-for-service-life-design-pdf-detail.html) \cite{fib.2006}. a model is explained that describes the carbonation depth $x_c$ [mm]  not only with the carbonation coefficient $k$ but also with a function $W(t)$  that takes into account additional sprinkling events of the component. The model is based on the principle of limit state. The fib Model Code specifies a fully probabilistic method and a method with partial safety factors for applying the model. When the model is applied probabilistically. the partial certainty coefficients $\gamma_R$ and $\gamma_{RH}$ can be set equal to 1. 


$$x_c(t)=\sqrt{2\cdot k_e\cdot k_c\cdot\gamma_R\cdot R^{-1}\cdot C_S}\cdot W(t)\cdot \sqrt{t}$$

$t$: [years] time

$\gamma_R$:  partial safety factor for $R^{-1}$, $\gamma_R=1.5$ [-]

$k_e$:  environmental function [-] 

$$k_e=\Biggl(\frac{1-\Bigl(\frac{RH_{real}}{\gamma_{RH}\cdot100}\Bigr)^{f_e}}{1-\Bigl(\frac{RH_{ref}}{100}\Bigr)^{f_e}}\Biggr)^{g_e}$$


 - $RH_{real}$:  relative humidity of the carbonated layer [\%]

 - $RH_{ref}$:  reference relative humidity, $RH_{ref}=65$ [\%] 

 - $g_e$:  exponent, $g_e=2.5$ [-] 

 - $f_e$:  exponent, $f_e=5.0$ [-] 

 - $\gamma_{RH}$:  partial safety factor for $RH_{real}$, $\gamma_{RH}=1.3$ [-]



$k_c$:  execution transfer parameter [-] 

 - In the probabilistic application of the model, the function for $k_c$  should be used. 

    $$k_c=\Bigl(\frac{t_c}{7}\Bigl)^{b_c}$$

    - $t_c$:  period of curing [days]

    - $b_c$:  exponent of regression, $b_c=-0.567$ [-]

- For the application with partial safety values, the values for $k_c$ from the table can be used. $k_c$ is dependent on $t_c$ if facty factors are used.
  
| $t_c$ [days] | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | 12   | 13   | 14   |
|--------------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| $k_c$ [-]    | 3.00 | 2.03 | 1.61 | 1.37 | 1.20 | 1.09 | 1.00 |0.92 | 0.86 | 0.81 | 0.77 | 0.73 | 0.70 | 0.67 |



$C_S$:  enviornmental impact ($CO_2$ concentration) 

$$C_S=C_{S,atm}+C_{S,emi}$$

 - $C_{S,atm}$:  $CO_2$ concentration of the atmosphere [kg/m³]

 - $C_{S,emi}$:  additional $CO_2$ concentration due to emission sources [kg/m³]

$W(t)$: [-]  factor/subfunction allowing for the effect of wetting events that will partly inhibit further ingress of $CO_2$ 

$$W(t)=\Bigl(\frac{t_0}{t}\Bigl)^{\frac{\bigl(p_{SR}\cdot ToW\bigr)^{b_w}}{2}} $$

-  $t_0$:       time of reference $t_0=0.0767$ [years]

 - $p_{SR}$:  probability of driving rain [-]

| location and orienation of element|$p_{SR}$|
|---|----|
|vertical elements| must be evaluated using weather station data|
|for horizontal elements| 1|
|for inner elements| 0 |

 - $b_w$:  exponent of regression, $b_w=0.446$ [-]

 - $ToW$:   avert number of rainy days per year [-] (Eq. \ref{fib_ToW}). A rainy day is defined by a minimum amount of precipitation water >= 2.5 mm per day 
$ToW=\frac{\text{Days with precipitation} h_{Nd} \geq \text{2,5mm per year}}{\text{365}}$

The inverse carbonation resistance $R^{-1}$ can be determined by accelerated (ACC) or natural (NAC) carbonation tests. The relationship between $R_{NAC,0}^-1$ and $R_{ACC,0}^{-1}$ is shown by the following equation:

$R^{-1}$:  inverse effective carbonation resistance of dry concrete 

$$R_{NAC,0}^{-1}=k_t\cdot R_{ACC,0}^{-1}+\epsilon_t$$


 - $R_{NAC,0}^{-1}$:  inverse effective carbonation resistance of dry concrete (RH=65\%)  determined at a certain point of time $t_0$ on specimens with the normal    carbonation test NAC [(mm²/years)/(kg/m³)] 

 - $R_{ACC,0}^{-1}$:  inverse effective carboation resistance of dry concrete, determinded at a    certain point of time $t_0$ on specimens with the accelerated    carbonation test ACC [(mm²/years)/(kg/m³)]

 - $k_t$:  regression parameter which considers the influence of test method on the ACC-test, $k_t=1.25$ [-]

 - $\epsilon_t$:  error term condicering inaccuracies which occur conditionally  when using the ACC test method, $\epsilon_t=315.5$ [(mm²/years)/(kg/m³)] 

 | Variable Name | Doc                                               | Unit             | GUI Key                               |
|---------------|---------------------------------------------------|------------------|---------------------------------------|
| RH            | relative humidity                                 | %                | Relative Humidity                     |
| ToW           | time of wetness (number of days with h_Nd>=2.5mm in a year) | day              | Time of Wetness                       |
| p_dr          | probability of driving rain                      | %                | Probability of Driving Rain            |
| t_c           | curing time                                       | day              | Curing Time                           |
| R_NAC         | inverse effective carbonation resistance (with normal carbonation test NAC) | mm²/year        | Inverse Effective Carbonation Resistance R^-1_ACC |
| CO2           | CO2 concentration by weight of CO2               | %                | CO2 Concentration                     |
| y_R           | safety factor for R                               | count            |                                       |
| y_RH          | safety factor for RH                              | [-]              |                                       |
| b_c           | exponent of regression                            | [-]              |                                       |
| b_w           | exponent of regression                            | [-]              |                                       |


### FibGuiglia: uses extension of Guiglia and Taliano (2013)

A formula designed by [Guiglia and Taliano](https://www.sciencedirect.com/science/article/pii/S0958946513000334) \cite{Guiglia.2013} to calculate inverse effective carbonation resistance with compressive strength $f_{c}$ can also be used:

$$R^{-1}_{NAC,0}=f^{-2.1}_{c} \cdot 10^7$$

- $f_{c}$: [MPa] compressive strength

| Variable Name | Doc                                                           | Unit   | GUI Key                     | Min Value | Max Value |
|---------------|---------------------------------------------------------------|--------|-----------------------------|-----------|-----------|
| RH            | relative humidity                                             | %      | Relative Humidity           |           |           |
| ToW           | time of wetness (number of days with h_Nd>=2.5mm in a year)   | day    | Time of Wetness             |           |           |
| p_dr          | probability of driving rain                                  | %      | Probability of Driving Rain | 0         | 100       |
| t_c           | curing time                                                   | days   | Curing Time                 |           |           |
| f_c           | mean value of the concrete compressive cylinder at 28 days   | MPa   | Compressive Strength       |           |           |
| CO2           | peripheral concentration by weight of CO2                   | %      | CO2 Concentration           |           |           |
| y_R           | safety factor for R                                           | [-]    |                             |           |           |
| y_RH          | safety factor for RH                                          | [-]    |                             |           |           |
| b_c           | exponent of regression                                        | [-]    |                             |           |           |
| b_w           | exponent of regression                                        | [-]    |                             |           |           |


## FibGreveDierfeld: used $k_{NAC}$ from Greve-Dierfeld and Gehlen  (2016)

Von [Greve-Dierfeld and Gehlen](https://onlinelibrary.wiley.com/doi/abs/10.1002/suco.201600085J) \cite{GreveDierfeld.2016a,GreveDierfeld.2016b,GreveDierfeld.2016c} have developed a model based on the [fib Model Code for Service Life Design](https://www.fib-international.org/publications/fib-bulletins/model-code-for-service-life-design-pdf-detail.html) \cite{fib.2006} through natural carbonation tests. The crabonation depth $x_c$ [mm] is given as:


$$x_c(t)=\gamma_f \cdot k_{NAC} \cdot \sqrt{k_e \cdot k_c \cdot k_a} \cdot W(t) \cdot \sqrt{t}$$

$t$: [years] time

$k_{NAC}$: [mm/$year^{0.5}$]  carbonation rate for standard test conditions 
- **Note:** The App uses the upper $k_{NAC}$ value of each resistance class, to predict a conservative carbonation depth.

| Resistance class | RC2 | RC3 | RC4 | RC5 | RC6 | RC7 |
|------------------|-----|-----|-----|-----|-----|-----|
| Ranges of $k_{NAC} $ | 1 < $k_{NAC}$ ≤ 2 | 2 < $k_{NAC}$ ≤ 3 | 3 < $k_{NAC}$ ≤ 4 | 4 < $k_{NAC}$ ≤ 5 |5 < $k_{NAC}$ ≤ 6 | 6 < $k_{NAC}$ ≤ 7 |    
| *Cement type*      | Water / Binder [-] | Water / Binder [-] | Water / Binder [-] | Water / Binder [-] | Water / Binder [-] | Water / Binder [-] |
| CEM I            | 0.45 | 0.50 | 0.55 | 0.60 | 0.65 | -   |
| CEM II/A         | 0.45 | 0.50 | 0.55 | 0.60 | 0.65 | -   |
| CEM II/B         | 0.40 | 0.45 | 0.50 | 0.55 | 0.60 | 0.65 |
| CEM III/A        | 0.40 | 0.45 | 0.50 | 0.55 | 0.60 | 0.65 |
| CEM III/B        | -   | 0.40 | 0.45 | 0.50 | 0.55 | 0.60 |




$k_e$: [-] factor/subfunction allowing for the environmental effect of relative humidity  $RH$ on the effective inverse carbonation resistance 

$$k_e=\Biggl(\frac{1-\Bigl(\frac{RH_{real}}{\gamma_{RH}\cdot100}\Bigr)^{f_e}}{1-\Bigl(\frac{RH_{ref}}{100}\Bigr)^{f_e}}\Biggr)^{g_e}$$

 - $RH_{real}$: [\%] relative humidity of the carbonated layer 

 - $RH_{ref}$: [\%]   reference relative humidity, $RH_{ref}=65$ 

 - $g_e$:  [-]  exponent, $g_e=2.5$

 - $f_e$:  [-]  exponent, $f_e=5.0$ 

 - $\gamma_{RH}$:  partial safety factor for $RH_{real}$, $\gamma_{RH}=1.3$ [-]

$k_c$: [-] factor/subfunction allowing for the effect of curing/execution (time of curing $t_c$)  on the effective carbonation resistance 

$$k_c=\Bigl(\frac{t_c}{7}\Bigl)^{b_c}$$

- $t_c$: [days] period of curing 

- $b_c$:  [-] exponent of regression, $b_c=-0.567$ 

$k_a$: [-]  factor/subfunction allowing for the effect of $CO_2$ concentration in the  ambient air 

$$k_a=\frac{C_a}{C_1}$$

- $C_a$: [vol-\%] $CO_2$ concentration of the ambient air  

- $C_1$: [vol-\%]  $CO_2$ concentration during concrete testing $C_1=0.04$ 


$W(t)$: [-]  factor/subfunction allowing for the effect of wetting events that will partly inhibit further ingress of $CO_2$ 

$$W(t)=\Bigl(\frac{t_0}{t}\Bigl)^{\frac{\bigl(p_{SR}\cdot ToW\bigr)^{b_w}}{2}} $$

-  $t_0$:   [years]    time of reference $t_0=0.0767$ 

- $p_{SR}$:[-]  probability of driving rain 

   | location and orienation of element|$p_{SR}$|
   |---|----|
   |vertical elements| must be evaluated using weather station data|
   |for horizontal elements| 1|
   |for inner elements| 0 |

 - $b_w$: [-] exponent of regression, $b_w=0.446$ 

 - $ToW$:  [-] avert number of rainy days per year [-] (Eq. \ref{fib_ToW}). A rainy day is defined by a minimum amount of precipitation water >= 2.5 mm per day 
$ToW=\frac{\text{Days with precipitation} h_{Nd} \geq \text{2,5mm per year}}{\text{365}}$

$\gamma_f$: safety factor [-] 

The safety factor $\gamma_f$ can be chosen for a deterministic application of the model from the Table. This ensures that the model has a certain reliability. 
In a probabilistic application $\gamma_f$ can be set equal to 1. 

| Exposure class | $\gamma_f$ |
|---------------|-----------|
| XC2, XC4      | 1.25      |
| XC3           | 0.70      |

| Variable Name | Doc                                                           | Unit   | GUI Key                     | One Of                                       | Min Value | Max Value |
|---------------|---------------------------------------------------------------|--------|-----------------------------|----------------------------------------------|-----------|-----------|
| RH            | relative humidity                                             | %      | Relative Humidity           |                                              |           |           |
| CEM           | cement type                                                   |        | Cement Type                 | CEM I, CEM II/A, CEM II/B, CEM III/A, CEM III/B |           |           |
| wb            | water / binder ratio                                         | count  | Water/Binder Ratio          |                                              | 0         | 1         |
| ToW           | time of wetness (number of days with h_Nd>=2.5mm in a year)   | days   | Time of Wetness             |                                              |           |           |
| p_dr          | probability of driving rain                                  | %      | Probability of Driving Rain |                                              | 0         | 100       |
| t_c           | curing time                                                   | day    | Curing Time                 |                                              |           |           |
| CO2           | peripheral concentration by weight of CO2                   | %      | CO2 Concentration           |                                              |           |           |
| y_f           | safety factor depending on exposure class                    | [-]    |                             |                                              |           |           |
| b_c           | exponent of regression                                        | [-]    |                             |                                              |           |           |
| b_w           | exponent of regression                                        | [-]    |                             |                                              |           |           |


## Guiglia and Taliano (2013)

The model of [Guiglia and Taliano](https://www.sciencedirect.com/science/article/pii/S0958946513000334) \cite{Guiglia.2013} is based on the [fib Model Code 2010](https://www.ernst-und-sohn.de/fib-model-code-for-concrete-structures-2010) and on an extensive experimental campaign. In this campaign, 1350 compressive tests were performed as well as measurements of the carbonation depth on concrete samples up to 5 years old from important infrastructure structures, such as bridges and tunnels. The tests refer to components protected from rain and the compressive strengths of the sampled concrete components ranged between 20 and 50 N/mm². 

The carbonation depth $x_c(t)$ [mm] is described by Guiglia and Taliano as follows: 

For **abutments and piers**: 
$$x_c(t)=163\cdot\sqrt{k_e\cdot f_{cm}^{-2,1}} \sqrt{t} $$

For **tunnels**:
$$x_c(t)=206\cdot\sqrt{k_e\cdot f_{cm}^{-2,1}} \sqrt{t}$$

$t$: [years]  t of the structure 

$k_e$: [-] environmental function

$$k_e=\Biggl(\frac{1-\Bigl(\frac{RH_{real}}{\gamma_{RH}\cdot100}\Bigr)^{f_e}}{1-\Bigl(\frac{RH_{ref}}{100}\Bigr)^{f_e}}\Biggr)^{g_e}$$

 - $RH_{real}$:  [\%] relative humidity of the carbonated layer 

 - $RH_{ref}$:  [\%]  reference relative humidity, $RH_{ref}=65$ 

 - $g_e$:  [-]  exponent, $g_e=2.5$ 

 - $f_e$:  [-] exponent, $f_e=5.0$ 

 - $\gamma_{RH}$: [-] partial safety factor for $RH_{real}$, $\gamma_{RH}=1.3$ 

$f_{cm}$: [MPa] mean value of the concrete compressive cylinder strenghth at 28 days 

| Variable Name | Doc                             | Unit | GUI Key           | One Of          |
|---------------|---------------------------------|------|-------------------|-----------------|
| f_c           | 28-day compressive strength     | MPa | Compressive Strength |               |
| RH            | relative humidity               | %    | Relative Humidity |               |
| building      | building types                  |      | Building Type     | Tunnel, others |


## Häkkinen (1993)
In [DuraCrete (1998)](https://books.google.de/books/about/Compliance_Testing_for_Probabilistic_Des.html?id=NY9CHAAACAAJ&redir_esc=y) \cite{DuraCrete.1998} an experimental model according to Häkkinen (1993) is explained, which describes the carbonation coefficient by the compressive strength. In addition, the model includes parameters and coefficients that depend on the type of cement, protection from rain, and whether air entraining materials were used for the concrete. The carbonation depth $x_c(t)$ [mm] is described as follows:

$$x_c(t)=c_{env}\cdot c_{air}\cdot a \cdot f_{cm}^b \cdot\sqrt{t}$$

$t$: [years] time

$C_{env}$: environmental coefficient 

   |exposure conditions|$C_{env}$|
   |--|-------|
   |structure sheltered from rain  | 1.0 |
   |structures exposed to rain |0.5|


$C_{air}$: air content coefficient 

   |	air entrained|$C_{air}$|
   |--|-------|
   |air entrained concrete | 1.0 |
   |not air entrained concrete|0.7|



$f_{cm}$: [MPa]mean compressive strength of the concrete at the t of 28 days 

$a$, $b$: parameters relating to cement type
- **Note:** In the App the *Binder type* is calculated with the mass fraction of OPC, fly ash,  silicia fume and blast furnace slag.

| Binder type                       | a | b |
|----------------------------------|-------|-------|
| Portland cement (OPC)           | 1800  | -1.7  |
| P.C. + 28% fly ash               | 360   | -1.2  |
| P.C. + 9% silica fume            | 400   | -1.2  |
| P.C. + 70% blast furnace slag    | 360   | -1.2  |

| Variable Name | Doc                            | Unit            | GUI Key                       | One Of                        |
|---------------|--------------------------------|-----------------|-------------------------------|-------------------------------|
| f_c           | 28-day compressive strength    | MPa            | Compressive Strength          |                               |
| ExCo          | exposure conditions            |                 | Exposure Condition            | Exposed, Sheltered, Indoor    |
| AirEntrained  | air entrained                  |                 | Air Entrained                 | Air Entrained, Not Air Entrained |
| C             | OPC content                    | kg/m³        | Portland Cement Content       |                               |
| FA            | fly ash content                | kg/m³        | Fly Ash Content               |                               |
| SF            | silicia fume content           | kg/m³        | Silica Fume Content           |                               |
| GGBS          | blast furnace slag content     | kg/m³        | Blast Furnace Slag Content     |                               |


## Hills et al. (2015) 
[Hills et al.](https://www.sciencedirect.com/science/article/pii/S0008884615000496) \cite{Hills.2015} have established two models for determining the carbonation coefficient $k$ of concrete. These carbonation models are based on statistical modeling as well as 43 different literature sources where carbonation depth was reported on different concrete structures, excluding accelerated carbonation depth studies because, according to Hills et al. it has not been demonstrated that these studies describe natural carbonation progress. The crabonation depth $x_c$ [mm] is given as:

$$x_c = e^{ln(k)} \cdot \sqrt{t}$$

- $t$: [years] time

- $ln(k)$: [$ln(\frac{mm}{year^{0.5}})$] carbonation coefficent

### Hills_time: time-dependent model
This model concentrates on the origin of the concrete and its age.
A quadratic term for concrete age $t$ [years] was included in the model to account for the nonlinear relationship between $t$ and $ln (K)$.


$$ln(k)=0.567-0.167\cdot I_{CEMI}+0.101\cdot I_{GGBS}+0.129\cdot I_{PFA} +0.249\cdot I_{Exposed}+0.818\cdot I_{Sheltered}+0.433\cdot I_{Indoor} +(0.037-0.088I_{Experimental})\cdot t+(-0.00046+0.0013\cdot I_{Experimental})\cdot t^2$$

The $I$ variables can only ever be 1 or 0. 
If the index of the $I$-variables for the used concrete matches the value of the respective variable is 1, if it does not match the variable has the value 0. 

- $I_{CEMI}$ contains concrete made with CEM I, or Ordinary Portland Cement (generally around 95% clinker and 5% gypsum)?

- $I_{GGBS}$ contains concrete made with CEM III, i.e. cement which contains some amount of blast furnace slag?

- $I_{PFA}$ contains concrete made with cement containing pulverised fly ash?

- $I_{Exposed}$ concrete that was outside and has been directly exposed to wind, rain and sun?

- $I_{Sheltered}$ concrete that was outside but not directly exposed to wind, rain and sun?

- $I_{Indoor}$ concrete that was kept indoors?

- $I_{Experimental}$ contains concrete cast specifically for carbonation tests?

| Variable Name | Doc                      | Unit | GUI Key        | One Of                              |
|---------------|--------------------------|------|----------------|-------------------------------------|
| mixture       | binder of concrete       |      | Mixture        | CEM I, OPC + Blast Furnace Slag, OPC + Fly Ash |
| ExCo          | exposure conditions      |      | Exposure Condition | Exposed, Sheltered, Indoor           |
| origin        | origin of the concrete   |      | Origin         | Structural, Experimental            |


### Hills_fc: Strength-dependent model 
This model is based on the exposure conditions, compressive strength and cement type.

$$ln(k)=1.066+1.761\cdot I_{CEMI}+2.062\cdot I_{GGBS}+2.061\cdot I_{PFA} -0.639\cdot I_{Exposed}-0.182\cdot I_{Sheltered}-0.648\cdot I_{Indoors} +(0.025-0.053\cdot I_{CEMI}-0.052\cdot I_{GGBS}-0.050\cdot I_{PFA})*f_c$$

- $f_c$ [MPa] compressive strength 

The $I$ variables can only ever be 1 or 0. 
If the index of the $I$-variables for the used concrete matches the value of the respective variable is 1, if it does not match the variable has the value 0. 

- $I_{CEMI}$ contains concrete made with CEM I, or Ordinary Portland Cement (generally around 95% clinker and 5% gypsum)?

- $I_{GGBS}$ contains concrete made with CEM III, i.e. cement which contains some amount of blast furnace slag?

- $I_{PFA}$ contains concrete made with cement containing pulverised fly ash?

- $I_{Exposed}$ concrete that was outside and has been directly exposed to wind, rain and sun?

- $I_{Sheltered}$ concrete that was outside but not directly exposed to wind, rain and sun?

- $I_{Indoor}$ concrete that was kept indoors?

| Variable Name | Doc                                | Unit   | GUI Key            | One Of                                          |
|---------------|------------------------------------|--------|--------------------|-------------------------------------------------|
| mixture       | content of concrete                |        | Mixture            | CEM I, OPC + Blast Furnace Slag, OPC + Fly Ash |
| ExCo          | exposure conditions                |        | Exposure Condition| Exposed, Sheltered, Indoor                     |
| f_c           | 28-day compressive strength        | MPa   | Compressive Strength|                                                 |


## Possan et al. (2021)
The model of [Possan et al.](https://www.semanticscholar.org/paper/Model-to-Estimate-Concrete-Carbonation-Depth-and-Possan-Andrade/6a4849fd5b61d1a4646c38c82d4724ba25acb679) \cite{Possan.2021} was obtained by coupling the concrete conduct equations reported in the literature, especially the first Fick’s Law. To adjust the model’s coefficients and parameters, 1298 data obtained through experts’ knowledge were used.
The following previously studied relationships and common assumptions for the empirical model, parameters and coefficients were assumed by Possan et al. :
- The carbon dioxide penetration is proportional to the compressive strength of the concrete.
- The carbonation proceeds more slowly when a larger number of carbonable products are available.
- The compressive strength is supposed to be highly related to the water-cement ratio, therefore, of the two influencing factors, only the compressive strength is considered.
- Carbonation depends on the moisture in the pores of the concrete and can progress best in pores partially filled with water.
- Carbonation occurs faster inside than outside, and concrete protected from rain carbonates faster than unprotected concrete.
- Carbonation causes the pores of concrete to narrow, which is why $CO_2$ transport becomes more difficult with age. 

The carbonation dpeth $x_c$ can be calculated with:

**Note:** Equation according *Corrigendum: Error in partial equation (13)* 

$$x_c=k_c \cdot \Bigl( \frac{20}{f_c} \Bigl) ^{k_{fc}} \cdot \Bigl( \frac{t}{20} \Bigr) ^{\frac{1}{2}} \cdot \exp \Biggl[ \Biggl( \frac{k_{ad} \cdot ad^{\frac{3}{2}}}{40+f_c} \Biggr) +\Biggl( \frac{k_{CO_2}*CO_2^{\frac{1}{2}}}{60+f_c} \Biggr) -\Biggl( \frac{k_{RH} \cdot (RH-0.58)^2}{100+f_c} \Biggr) \Biggr]  \cdot k_{ce}$$

$t$: [years] time

$RH$: [\%] relative humidity  

$CO_2$: [\%] $CO_2$ content in the atmosphere 

$f_c$: [MPa]  concrete compressive strenght 

$ad$: [\%] puzzolanic addition in concrete related to cement mass 

$k_{ce}$: [-] variable factor regarding the rain protection 

   | Exposure condition          | $k_{ce}$ |
   |-----------------------------|---------|
   | Indoor                      | 1.30    |
   | Outdoor, sheltered from rain | 1.00    |
   | Outdoor, exposed to rain    | 0.65    |


$k_c$: [-] variable factor regarding the cement type 

$k_{fc}$: [-]  variable factor regarding concretes compressive strenght 

$k_{ad}$: [-] variable factor regarding puzzolanic addition in concrete 

$k_{CO_2}$: [-] variable factor regarding environment's $CO_2$ 

$k_{RH}$: [-]  variable factor regarding felative humidity 

**Note:** Table according *Corrigendum: Error in model coefficients table* 

|    cement type            | $k_c$ |$k_{fc}$| $k_{ad}$| $k_{CO_2}$ | $k_{RH}$ |
|---------------            |----   |------ |----- |-----   |------|
| CEM I                     | 19.8  | 1.7   | 0.24 | 18.0   |1300  |
| CEM II/A-L                | 21.68 | 1.5   | 0.24 | 18 .0  |  1100|
| CEM II/A-S, CEM II/B-S    | 22.48 | 1.5   |  0.32| 15.5   | 1300 |
| CEM II/A-V                | 23.66 | 1.5   | 0.32 | 15.5   | 1300 |
| CEM III/A                 | 30.50 | 1.7   | 0.32 | 15.5   | 1300 |
| CEM IV/A,  CEM IV/B       | 33.27 | 1.7   | 0.32 | 15.5   | 1000 |

| Variable Name | Doc                                                                       | Unit   | GUI Key                       | One Of                                                 | Min Value | Max Value |
|---------------|---------------------------------------------------------------------------|--------|-------------------------------|--------------------------------------------------------|-----------|-----------|
| ad            | puzzolanic addition content (silica fume, metakaolin, rice husk ash) related to total binder mass in [%] | %      | Puzzolanic Addition Content   |                                                        | 0         | 100       |
| CEM           | cement type                                                               |        | Cement Type                   | CEM I, CEM II/A-L, CEM II/A-S, CEM II/B-S, CEM II/A-V, CEM III/A, CEM IV/A, CEM IV/B |           |           |
| f_c           | concrete compressive strength                                             | MPa   | Compressive Strength          |                                                        |           |           |
| ExCo          | exposure conditions                                                      |        | Exposure Condition            | Exposed, Sheltered, Indoor                           |           |           |
| CO2           | CO2 content in the atmosphere                                             | %      | CO2 Concentration             |                                                        |           |           |
| RH            | relative humidity                                                         | %      | Relative Humidity             |                                                        |           |           |



## Silva et al. (2014)

This model presented by [Silva et al.](https://www.sciencedirect.com/science/article/pii/S095894651300200X) \cite{Silva.2014} for calculating the carbonation depth of concrete is based on previous studies. From a total of 17 studies, 964 specimens with a wide range of concrete and environmental characteristics were used to build the model. The carbonation coefficient $k$ is described differently for two different relative humidity ranges ($RH$).
Exposure class XC2 corresponds to situations where the humidity is above 70\%.
The carbonation depth $x_c$ [mm] is given as:

$$x_c=k\cdot \sqrt{t}$$

$t$: [years] time


For **$RH$ > 70\%**:
$$k=3.355\cdot CO_2\cdot 0.019\cdot C-0.042\cdot f_{c}+10.83$$

For **RH $\leq$ 70 \%**:
$$ k=0.556\cdot CO_2\cdot X-0.148\cdot f_{c}+18.734 $$


$CO_2$: [\%]  $CO_2$-content 

$C$:  [kg/m³]  clinker content 

$f_{c}$:  [MPa] 28-day compressive strenght 

$X$: [-] exposure class factor 

   | Exposure Class | X |
   |---------------|---|
   | XC1           | 1 |
   | XC2           | - |
   | XC3           | 2 |
   | XC4           | 3 |

| Variable Name | Doc                              | Unit            | GUI Key                | One Of             | Min Value | Max Value |
|---------------|----------------------------------|-----------------|------------------------|--------------------|-----------|-----------|
| C             | clinker content                  | kg/m³        | Clinker Content        |                    |           |           |
| f_c           | 28-day compressive strength      | MPa            | Compressive Strength   |                    |           |           |
| ExpC          | exposure class                   |                 | Exposure Class         | XC1, XC2, XC3, XC4 |           |           |
| RH            | relative humidity                | %               | Relative Humidity      |                    | 0         | 100       |
| CO2           | CO2 content                      | %               | CO2 Concentration      |                    |           |           |


## Ta et al. (2016)

[Ta et al.](https://www.semanticscholar.org/paper/A-new-meta-model-to-calculate-carbonation-front-Ta-Bonnet/b6e64b5ad6a7725f3e2c3b81998524024ff528d4) \cite{Ta.2016} have developed a model that takes into account many factors that influence the carbonation of concrete.  
The model is based on many previously researched or designed relationships and formulas. Some formulas have been adapted to make the model widely applicable.  
However, there are some **limitations** for the model to be applied:
- The water-cement ratio, or water-binder ratio $\frac{W}{C}$ must be only in the range 0.5<$\frac{W}{C}$<0.8. 
- The model is defined only for maximum grain sizes $S_{max}$ between 8 and 31.5mm. 
  
The carbonation depth $x_c$ [mm] is given as:

$$x_c=\sqrt{\frac{2 \cdot D_{CO_2} \cdot CO_2}{a}} \cdot \sqrt{t}$$

 $t$: [years] time

$CO_2$: [kg/m³]  $CO_2$ concentration in the air 

$a$: [kg/m³]  amount of $CO_2$ absorbed 

$$a = 0.75 \cdot C\cdot CaO \cdot \phi_{clinker} \cdot \frac{M_{CO_2}}{M_{CaO}}$$

- $C$:  cement content [kg/m³] 
- $CaO$:  amount of calcium oxide per weight of cement [-] 
- $\phi_{clinker}$:  cement clinker content [-] 
- $M_{CO_2}$:  Molar weight of $CO_2$ [g/mol] **Note:** In App = 44.01 g/mol
- $M_{CaO}$:  Molar weight of CaO [g/mol] **Note:** In App = 56.0774 g/mol



$D_{CO_2}$: [mm²/year] $CO_2$ diffusion coefficient 

$$D_{CO_2} = D_{CO_2}^{28} \cdot f(RH) \cdot f(T) \cdot f(\frac{(S+G)}{C}) \cdot f(\phi, w/c, FA) \cdot f(t_c) *365*24*60*60*1000^2$$
 
 - $f(RH)$: [-]

$$f(RH)=\left(1-\frac{RH}{100}\right)^2 \cdot \left(\frac{RH}{100}\right)^{2.6}$$
  - $RH$: [\%] relative external humidity 

- $f(T)$: [-]

$$f(T)=e^{\frac{4700(T -293)}{293 \cdot T}}$$
   -  $T$:  [°C]  temperature 

- $f(\frac{(S+G)}{C})$: [-]

  $$f(\frac{(S+G)}{C}) = \left(\frac{(S+G)}{C}\right)^{0.1} $$
   - $S$:  [kg/m³] sand content 
   - $G$:  [kg/m³] gravel content 

- $f(\phi, w/c, FA)$: [-]
    $$f(\phi, w/c, FA)= f(w/c) \cdot \left[ \frac{(0.93-3.95 \cdot 0.94^{100 \cdot w/c})\cdot \phi - \phi_{air}}{\frac{W}{\rho_w} \cdot \frac{C}{\rho_c} \cdot \frac{FA}{\rho_{FA}}} \right]^{1.8}$$

    - $\rho_w$: [kg/m³]  densitiy of water. Note in App: = 1000 kg/m³
    - $\rho_c$:  [kg/m³] densitiy of cement  
    - $\rho_{FA}$:  [kg/m³] densitiy of fly ash
    - $FA$: [kg/m³]  fly ash content of concrete. **Note:** In the particular case of CEM II cement type containing FA, FA value is taken to be zero.
 
    - $f(w/c)$: [-] see following equation:

    $$f(w/c)=2437.3 \cdot e^{-5.592 \cdot w/c}$$

    - $w/c$: [-] water binder ratio **Note:** for 0.5< w/c <0.8



- $\phi$ [-] is the carbonated concrete porosity
   $$ \phi = \phi_{air} + \frac{W}{\rho_w} - [0.249 \cdot (CaO -0.7\cdot SO_3) +0.191 \cdot SiO_2 +1.118 \cdot Al_2O_3 - 0.357 \cdot Fe_2O_3] *\frac{C}{1000} $$

    - $W$: [kg/m³] water content of concrete. Note: Is calculated in App from $w/c$ and $C$.
    - $SO_3$:  [-]  amount of sulfur oxide per weight of cement
    - $SiO_2$: [-] amount of silicon oxide per weight of cement  
    - $Al_2O_3$: [-]  amount of aluminium oxide per weight of cement 
    - $Fe_2O_3$: [-]  amount of iron oxide per weight of cement 
    - $\phi_{air}$: [-]   air content in concrete from Table.  Values can be interpolated.
      - $S_{max}$:  [mm] maximum nominal aggregate size 
 
         | $S_{max}$ | $\phi_{air}$|
         |---------------|-----------|
         |    31.5  |   0.015 |
         |      16.0     |0.023      |
         | 8.0   |0.035   |


 - $D_{CO_2}^{28}$: [m²/s]  $CO_2$ diffusion coefficient in concrete  
    $$D_{CO_2}^{28}= 10^{-7} \cdot 10^{-0.036\cdot f_c}$$
    -  $f_c$: [MPa]  28-day compressive strenght can be calculated with the following equation. **Note:** This eqiation is used in the App.
        $$ f_c= \frac{7.84 \cdot f_{CEM}}{(1 +w/c \cdot \frac{\rho_c}{\rho_w}+ \phi_{air} \cdot \frac{\rho_c}{C})^2}$$
        - $f_{cem}$:  standard strenght class of cement [MPa] 
  
  - $f(t_c)$: [-]

    $$f(t_c) = \frac{1.9 \cdot 10^{-2}}{10^{-0.025 \cdot f_c}}+\left( 1-\frac{1.9 \cdot 10^{-2}}{10^{-0.025 \cdot f_c}} \cdot \sqrt{\frac{28}{0.01 \cdot t_c}} \right)$$
 
    - $t_c$:  curing time [days]

| Variable Name | Doc                                                        | Unit          | GUI Key                          | Min Value | Max Value |
|---------------|------------------------------------------------------------|---------------|----------------------------------|-----------|-----------|
| C             | cement content (Binder=C+FA)                              | kg/m³     | Portland Cement Content          |           |           |
| p_c           | density of cement                                          | kg/m³     | Density of Portland Cement       |           |           |
| phi_clinker   | clinker content in cement                                  | count         | Clinker Content of Cement        |           |           |
| CaO           | amount of calcium oxide per weight of cement              | count         | CaO Content of Cement            | 0         | 1         |
| SO3           | amount of sulfur oxide per weight of cement               | count         | SO3 Content of Cement            | 0         | 1         |
| SiO2          | amount of silicon oxide per weight of cement              | count         | SiO2 Content of Cement           | 0         | 1         |
| Al2O3         | amount of aluminium oxide per weight of cement            | count         | Al2O3 Content of Cement          | 0         | 1         |
| Fe2O3         | amount of iron oxide per weight of cement                 | count         | Fe2O3 Content of Cement          | 0         | 1         |
| f_cem         | standard strength class of cement                         | MPa          | Compressive Strength of Cement   |           |           |
| wb            | water / binder ratio                                      | count         | Water/Binder Ratio               |           |           |
| FA            | fly ash content (if NOT included in CEM II)               | kg/m³     | Fly Ash Content                  |           |           |
| p_FA          | density of fly ash                                         | kg/m³     | Density of Fly Ash               |           |           |
| S             | sand content                                               | kg/m³     | Sand Content                     |           |           |
| G             | gravel content                                             | kg/m³     | Gravel Content                   |           |           |
| S_max         | maximum aggregate size                                     | mm           | Maximum Aggregate Size           |           |           |
| t_c           | curing period                                              | day           | Curing Time                      |           |           |
| RH            | relative humidity                                          | %             | Relative Humidity                | 0         | 100       |
| T             | temperature                                                | °C            | Temperature                      |           |           |
| CO2           | CO2 concentration                                          | %             | CO2 Concentration                |           |           |
| p_w           | density of water (init=False)                              | kg/m³     |                                  |           |           |
| M_CO2         | molar mass of CO2 (init=False)                            | g/mol         |                                  |           |           |
| M_CaO         | molar mass of CaO (init=False)                            | g/mol         |                                  |           |           |


## Yang et al. (2014)$CO_2$


This model by [Yang et al.](http://www.sciencedirect.com/science/article/pii/S0195925514000055) \cite{Yang.2014} is based on previously researched carbonation relationships as well as numerous surveys of concrete carbonation with some additional data, such as environmental conditions and service life expectations of the components. In addition, a study was conducted to investigate the absorption of $CO2$ of two buildings with different environmental conditions. The carbonation coefficient depends on the water-cement ratio as well as some factors that take into account the relative humidity, the surface materials on the concrete, and the substitution degree of supplementary cementitious materials (SCMs) on the diffusivity. The carbonation depth $x_c(t)$ is described as follows:


$x_c(t)=\sqrt{\frac{2D_{CO_2}(t)}{a_{CO_2}(t)}\cdot C_{CO_2}}$

$a_{CO_2}(t)$:  [g/cm³] amount of absorbable $CO_2$

- $a_{CO_2}(t)=\alpha_h(t)*M_{ct}(t)*M_{CO_2}*10^{-6}$


    - $\alpha_h(t)=\frac{t}{2.0+t}*\alpha_\infty$

    - $\alpha_\infty=\frac{1.031*\frac{W}{C}}{0.194+\frac{W}{C}}$

        - $\frac{W}{C}$: water-to-cement ratio [-]


-  $M_{ct}(t)$: [mol/cm³]  molar concentration of the carbonatable constituents of the paste per unit volume of concrete at t 

    - $M_{ct}(t)=8.06 \cdot C$

    - $C$: [kg/m³] cement content 

 $C_{CO_2}$:  [g/cm³] peripheral concentration by weight of $CO_2$ 
 
 $D_{CO_2}(t)$:  [mm²/year] diffusion coefficient of $CO_2$ at time $t$ [years]

- $ D_{CO_2}(t)=136.6\cdot \beta_s \cdot \beta_f\cdot \beta_h\cdot \Bigl(\frac{a}{C}\Bigr)^{0.1}+\bigl(\epsilon_p(t)\bigr)^2 \cdot (10^2 \cdot 365)$

    -  $\frac{a}{C}$: [-]  agreggate-to-cement ratio per weight 

    -  $\beta_s$: [-]  correction factor for the replacement of suppementary cementitious materials (SCMs) [-] for different SCM types.


|SCM replacement [%] | 0-10   | 10-20  | 20-30  | 30-40  | 40-50  | 50-80  |
|---------------------|--------|--------|--------|--------|--------|--------|
| Fly ash             | $\beta_s=$ 1.05   | $\beta_s=$ 1.05   | $\beta_s=$ 1.10   | $\beta_s=$ 1.10   | -      | -      |
| Blast furnace slag  | $\beta_s=$ 1.05   | $\beta_s=$ 1.10   | $\beta_s=$ 1.15   | $\beta_s=$ 1.20   | $\beta_s=$ 1.35   | $\beta_s=$ 1.40   |
| Silica fume         | $\beta_s=$ 1.05   | $\beta_s=$ 1.10   | -      | -      | -      | -      |

-  $\beta_f$:  [-] represents the delayed carbonation process due to finishing materials in dependence of the exposue location.


| finishing material and exposure condition | Nothing | Plaster (G) | Mortar (M) | Paint (P) | M+G  | M+P  | Tiles |
|------------------------------|---------|-------------|------------|-----------|------|------|-------|
|Indoor                        |$\beta_f=$ 1.0     | $\beta_f=$ 0.79        | $\beta_f=$ 0.29       | $\beta_f=$ 0.57      | $\beta_f=$ 0.41 | $\beta_f=$ 0.15 | $\beta_f=$ 0.21  |
| outdoor = [Sheltered, Exposed]                      |$\beta_f=$ 1.0      | -           |$\beta_f=$ 0.28        | $\beta_f=$ 0.8       | -    |  -   | $\beta_f=$ 0.7   |         



-  $\beta_h$:  [-] represents the effect of relative humidity on the $CO_2$ diffusion rate 

    - $\beta_h=\Bigl(1-\frac{RH}{100}\Bigr)^{0.6}$

    - $RH$: [\%] relative humidity 

- $\epsilon_p(t)$: [-]  total porosity of cement paste at t t [years]

    - $\epsilon_p(t)=\frac{0.1+2.62\Bigl(\frac{W}{C}\Bigr)^{4.2}\cdot t\cdot 365}{1.5\Bigl(\frac{W}{C}\Bigr)^2\cdot t\cdot 365}$



| Variable Name | Doc                                           | Unit          | GUI Key                | One Of                                                     | Min Value | Max Value |
|---------------|-----------------------------------------------|---------------|------------------------|------------------------------------------------------------|-----------|-----------|
| C             | cement content B=C+FA+GGBS+SF                 | kg/m³     | Portland Cement Content |                                                            |           |           |
| S             | sand content                                 | kg/m³     | Sand Content           |                                                            |           |           |
| G             | gravel content                               | kg/m³     | Gravel Content         |                                                            |           |           |
| FA            | fly ash content                              | kg/m³     | Fly Ash Content        |                                                            |           |           |
| GGBS          | ground granulated blast furnace slag content | kg/m³     |                        |                                                            |           |           |
| SF            | silica fume content                          | kg/m³     | Silica Fume Content    |                                                            |           |           |
| wb            | water / binder ratio                         | count         | Water/Binder Ratio     |                                                            |           |           |
| RH            | relative humidity                            | %             | Relative Humidity      |                                                            | 0         | 100       |
| ExCo          | exposure conditions                          |               | Exposure Condition     | Sheltered, Exposed, Indoor                               |           |           |
| Finishing     | finishing material                           |               | Finishing Material     | Nothing, Plaster, Mortar + Plaster, Mortar, Mortar + Paint, Tile, Paint |           |           |
| CO2           | CO2 concentration                            | %             | CO2 Concentration      |                                                            |           |           |
| M_CO2         | molar mass of CO2 (init=False)              | g / mol       |                        |                                                            |           |           |

