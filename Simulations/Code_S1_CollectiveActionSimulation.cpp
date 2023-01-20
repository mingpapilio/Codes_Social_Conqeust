/*
* @file Code_S1_CollectiveActionSimulation.cpp
*
* @organization Academia Sinica
* @author Ying-Yu Chen
* @contact yingyuchentw003@gmail.com
*/

#include <iostream>
#include <math.h>
#include <vector>
#include <random>
#include <chrono>
using namespace std;

// To generate random number
class RandGenerator{
public:
	RandGenerator();
	// to generate a random number from the continuous uniform distribution on the interval [start, end]
    double	RUnif(double Start, double End);
	// to select a random item from the list {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0} to determine an individual's degree of cooperation
	double	RandDeg();
	// to generate a random number from a Bernoulli distribution
    bool	RBern(double Prob);
	// to generate a random number from a 2D Gaussian distribution
	int		R2DGaussian();
	// to generate a random number from a uniform integer distribution on the interval [start, end-1]
	int		SampleInt(int Start, int End);
private:
	unsigned seed;
	default_random_engine RAND_GENERATOR;
};

class Individual{
public:
    Individual(int PatchID, double CoopDeg, int Age);
	void	Aging(){ _Age = _Age + 1; }
    void	UpdateReproRate(int    ReproRate){ _ReproRate = ReproRate; }
	void	UpdateSurvRate (double SurvRate ){ _SurvRate  = SurvRate;  }
	int		GetAge()        { return _Age;         }
    int		GetReproRate()  { return _ReproRate;   }
	double	GetSurvRate()   { return _SurvRate;    }
    double	GetCoopDeg()    { return _CoopDeg;     }

private:
	int		_Age;
    int     _PatchID;	// ID of the patch to which the individual belongs
    int     _ReproRate;	// reproduction rate
	double	_SurvRate;	// survival rate
    double  _CoopDeg;	// degree of cooperation
	RandGenerator RG;
};

class Patch{
public:
	Patch();
	// to add an individual to the patch
    void	AddIndividual(int PatchID, double CoopDeg, int Age);
	void	UpdateAge();
    void	UpdateCoopNum();
    void	UpdateCoopDegSum();
    void	UpdateResource		(double InitRes, double CoopEfficiency, double MaxIncreRate);
    void	UpdateIndivReproRate(double MetabolicConsump, double HalfConst, double ReproMax, double CostRate);
	void	UpdateIndivSurvRate (double SurvRateUL, double AgeStandard, double CostRate);
	void	UpdateAlive();
	// to get the size of the patch (or the number of the individuals in the patch)
	int		GetSize()		   		  { return _Individual.size();  }
    int		GetCoopNum()   		      { return _CoopNum;            }
	double	GetFlucRes()	   		  { return _FlucRes;           	}
    double	GetCoopDegSum()		      { return _CoopDegSum;	        }
	// to get all the offspring will be produced by all the individuals in the patch
	vector<double> GetOffspring();

private:
    int     _CoopNum;		// the number of cooperators in the patch
    double  _CoopDegSum;	// the sum of the degree of cooperation of all individuals in the patch
	double	_FlucRes;		// the fluctuating environmental resource availability
	double	_Resource;		// total resource gain (including the increment due to cooperation) of the patch
	vector<Individual> _Individual;
	RandGenerator RG;
};

// To manage processes in population level
class PopProcess{
public:
	PopProcess(int OutputType, double CoopEfficiency, double ResMean, double ResHalfVarRange, double CostRate, double InitCoopProp, int Replic, int Span, bool Sociality);
	~PopProcess();
	// to change the mean and the variation range of the environmental resource availability
	void	EnvChange(double ResMeanOffset, double ResHalfVarRangeOffset);
	// to compute the number of cooperators, the proportion of the cooperators, and average degree of cooperation at population level
    void	ComputePopCoopData();
	// to compute and print all information regarding the population status at the given time
    void    ComputeTimeSeriesData(int Time);
	// to handle cross-patches offspring dispersal (5*5 2D Gaussian kernel)
	void	OffspringDisperse();
	// to iteratively update the population until the EndTime
    void	SystemUpdate(int StartTime, int EndTime);
	// to handle the exception as the population go extinct
	void	ErrorHandling1();
	// to handle the exception as the population becomes larger than the upper limit
	void	ErrorHandling2();
	int		GetPopSize()				{ return _PopSize;	        }
    int		GetTotalCoopNum()   		{ return _TotalCoopNum;	    }
    double	GetCoopProp()   			{ return _CoopProp;		    }
    double	GetAverCoopDeg()    		{ return _AverCoopDeg;	    }
	vector<Patch>  GetPatch()			{ return _Patch;			}

private:
	// Population state
    int     _PopSize;			// population size
	int		_PatchNum;			// the number of patches in the population
    int		_PopSizeUL;			// the upper limit of the population size
    int		_TotalCoopNum;		// the total number of cooperators in the population
    double	_CoopProp;			// the proportion of cooperators in the population
	double	_InitCoopProp;		// the initial proportion of cooperators in the population
    double	_AverCoopDeg;		// average degree of cooperation
	
    // Population structure
	vector<Patch> _Patch;

	// Resource consumption
	double	_ResMean;			// the mean of the environmental resource availability
	double	_ResHalfVarRange;	// the half variation range of the environmental resource availability
    double	_CoopEfficiency;	// the efficiency of transfering cooperation efforts to cooperation benefits
    double  _MaxIncreRate;		// the maximum resource increment rate due to cooperation
	double	_MetabolicConsump;	// the metabolic consumption of each individual

	// Reproduction
    double  _HalfConst;			// the “half-saturation constant”, which is the value of the cooperation benefits at which the individual reproduction increment rate is half of its maximum
    double  _ReproMax;			// the maximum reproduction rate without cooperation
    double	_CostRate;			// the percentage decrease in the reproduction rate caused by per unit cooperation degree
	double	_Heritability;		// the probability that the offspring has the same degree of cooperation as its parent

	// Survival rate
	double	_AgeStandard;		// the exponential age constant to determine the exponential decay of the survival rate
    double	_SurvRateUL;		// the upper limit of survival rate
	
    // Random number generator
	RandGenerator RG;

    // For convenience of data computation
    int		_Span;				// the time interval which determines the frequency of the time series output
	int		_Replic;			// the serial number of the simulation replication
	int		_Length;			// the length of the square habitat
	int		_OutputType;		// 1: population final state; 2: time series of population state
};



void PopProcess::SystemUpdate(int StartTime, int EndTime){
	for (int time = StartTime; time < EndTime; time++){

        // to update all patches in the population
		double fluc_res = RG.RUnif(_ResMean-_ResHalfVarRange, _ResMean+_ResHalfVarRange);
		for (Patch& patch: _Patch){
			patch.UpdateAge();
            patch.UpdateCoopNum();
            patch.UpdateCoopDegSum();
			patch.UpdateResource(fluc_res, _CoopEfficiency, _MaxIncreRate);
            patch.UpdateIndivReproRate(_MetabolicConsump, _HalfConst, _ReproMax, _CostRate);
		}
		OffspringDisperse();
		for (Patch& patch: _Patch){
			patch.UpdateIndivSurvRate(_SurvRateUL, _AgeStandard, _CostRate);
			patch.UpdateAlive();
		}
		
        // to compute and check population size
		_PopSize = 0;
		for (Patch& patch: _Patch){
			_PopSize = _PopSize + patch.GetSize();
		}
		if (_PopSize == 0){
			ErrorHandling1();
            break;
		}
		if (_PopSize > _PopSizeUL){
			ErrorHandling2();
			break;
		}

		// to compute the number of cooperators, the proportion of the cooperators, and average degree of cooperation at population level
        ComputePopCoopData();

        // to compute time series data
		if ((time%_Span == _Span-1) && (_OutputType == 2)){
			ComputeTimeSeriesData(time);
		}
	}
}

class Simulation{
public:
	Simulation(int OutputType, double ResMean, double ResHalfVarRange, double ResMeanOffset, double ResHalfVarRangeOffset, double CoopEfficiency, double CostRate, \
			   double InitCoopProp, int EnvChangeTime, int EndTime, int InitReplic, int ReplicNum, int Span, bool Sociality);
	// to shunt the simulation to the different processes according to the output type
    void	ProcessShunt(int OutputType);
	// the process for the output of time series data
	void	PopTimeSeries();
	// the process for the output of population final states
	void	PopFinalState();

private:
	int		_OutputType;			// 1: population final state; 2: time series of population state
	int		_EnvChangeTime;			// the time when the mean and the variation range of the environmental resource availability. if _EnvChangeTime == _EndTime, no change happens.
	int		_EndTime;				// the end time of the simulation
	int		_InitReplic;			// the initial serial number of the simulation replication. Useful on restarts.
	int		_ReplicNum;				// Total number of replications
	int		_Span;					// the time interval which determines the frequency of the time series output
	bool	_Sociality;				// the sociality of the whole population
	double	_CostRate;				// the percentage decrease in the reproduction rate caused by per unit cooperation degree
	double	_InitCoopProp;			// the initial proportion of cooperators in the population
	double	_CoopEfficiency;		// the efficiency of transfering cooperation efforts to cooperation benefits
	double	_ResMean;				// the mean of the environmental resource availability
	double	_ResHalfVarRange;		// the half variation range of the environmental resource availability
	double	_ResMeanOffset;			// the change in the mean of the environmental resource availability (when environmental change happens)
	double	_ResHalfVarRangeOffset;	// the change in the half variation range of the environmental resource availability (when environmental change happens)
};



int main(int arc, char *argv[]){

    int     output_type, env_change_time, end_time, init_replic, replic_num, span;
    bool    sociality;
    double  res_mean, res_half_var_range, coop_efficiency, cost_rate, init_coop_prop, res_mean_offset, res_half_var_range_offset;
	
	cin >> output_type;

	// to print headers
	if (output_type == 1){
		cout << "pop_size_before,coop_num_before,noncoop_num_before,coop_prop_before,aver_coop_deg_before,coop_efficiency,cost_rate,res_mean,res_var_range,sociality,replic,pop_size,coop_num,noncoop_num,coop_prop,aver_coop_deg,init_coop_prop";
	}else if (output_type == 2){
		cout << "coop_efficiency,cost_rate,res_mean,res_var_range,replic,time,pop_size,coop_num,noncoop_num,coop_prop,aver_coop_deg,init_coop_prop";
	}
	for (int var_type = 0; var_type < 4; var_type++){
		for (int patch_id = 0; patch_id < 529; patch_id++){
			cout << ",";
			switch (var_type)
			{
				case 0:{
					cout << "pop_size_" << patch_id;
				}break;
				case 1:{
					cout << "coop_num_" << patch_id;
				}break;
				case 2:{
					cout << "coop_deg_sum_" << patch_id;
				}break;
				case 3:{
					cout << "res_" << patch_id;
				}break;
			}
		}
	}
	cout << "\n";

    while (cin >> res_mean >> res_half_var_range >> res_mean_offset >> res_half_var_range_offset >> coop_efficiency >> cost_rate >> init_coop_prop >> env_change_time \
			   >> end_time >> init_replic >> replic_num >> span >> sociality){
        Simulation Sim(output_type, res_mean, res_half_var_range, res_mean_offset, res_half_var_range_offset, coop_efficiency, cost_rate, init_coop_prop, \
					   env_change_time, end_time, init_replic, replic_num, span, sociality);
	    Sim.ProcessShunt(output_type);
    }
	
	return 0;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////

RandGenerator::RandGenerator(){
	seed = chrono::system_clock::now().time_since_epoch().count();
	RAND_GENERATOR.seed(seed);
}

double RandGenerator::RUnif(double Start, double End){
	uniform_real_distribution<double> distribution(Start, End);
	return distribution(RAND_GENERATOR);
}

double RandGenerator::RandDeg(){
    uniform_int_distribution<int> distribution(1, 10);
    double output = (double)distribution(RAND_GENERATOR)/10;
    return output;
}

bool RandGenerator::RBern(double Prob){
	bernoulli_distribution distribution(Prob);
	return distribution(RAND_GENERATOR);
}

int RandGenerator::R2DGaussian(){
	discrete_distribution<int>  distribution {0.003765, 0.015019, 0.023792, 0.015019, 0.003765, \
                                           	  0.015019, 0.059912, 0.094907, 0.059912, 0.015019, \
                                           	  0.023792, 0.094907, 0.150342, 0.094907, 0.023792, \
                                           	  0.015019, 0.059912, 0.094907, 0.059912, 0.015019, \
                                           	  0.003765, 0.015019, 0.023792, 0.015019, 0.003765};
	return distribution(RAND_GENERATOR);
}

int RandGenerator::SampleInt(int Start, int End){
	uniform_int_distribution<int> distribution(Start, End-1);
	return distribution(RAND_GENERATOR);
}

Individual::Individual(int PatchID, double CoopDeg, int Age){
	_Age            = Age;
	_PatchID        = PatchID;
	_CoopDeg        = CoopDeg;
	_ReproRate      = 0;

	if (_CoopDeg == -1.0){
		_CoopDeg = RG.RandDeg();
	}
}

Patch::Patch(){
}

void Patch::AddIndividual(int PatchID, double CoopDeg, int Age){
	_Individual.push_back(Individual(PatchID, CoopDeg, Age));
}

void Patch::UpdateCoopDegSum(){
	_CoopDegSum = 0.0;
	for (Individual& indiv: _Individual){
		_CoopDegSum = _CoopDegSum + indiv.GetCoopDeg();
	}
}

void Patch::UpdateCoopNum(){
	_CoopNum = 0;
	for (Individual& indiv: _Individual){
		if (indiv.GetCoopDeg() > 0.0){
			_CoopNum++;
    	}
	}
}

void Patch::UpdateAge(){
	for (Individual& indiv: _Individual){
		indiv.Aging();
	}
}

void Patch::UpdateResource(double InitRes, double CoopEfficiency, double MaxIncreRate){
    double coop_benefit = _CoopDegSum * CoopEfficiency;
	_FlucRes  = InitRes;
    _Resource = InitRes*(1 + MaxIncreRate*coop_benefit/(MaxIncreRate*InitRes/2 + coop_benefit));
}

void Patch::UpdateIndivReproRate(double MetabolicConsump, double HalfConst, double ReproMax, double CostRate){
    // to compute individual intake and reproduction increment rate
    double res_per_capita = _Resource/_Individual.size();
    double tmp = 0;
    if (res_per_capita > MetabolicConsump){
        tmp = (res_per_capita-MetabolicConsump)/(HalfConst+ res_per_capita-MetabolicConsump);
    }
	
	// to compute individual reproduction rate and total reproduction of the group
	for (Individual& indiv: _Individual){
		double	expected_repro_rate = ReproMax * tmp * (1.0 - CostRate*indiv.GetCoopDeg());
		double  repro_rate_floor = floor(expected_repro_rate);
		double  prob = expected_repro_rate - repro_rate_floor;
		int     indiv_repro;
		if (RG.RBern(prob)){
			indiv_repro = (int)(repro_rate_floor+1);
		}else{
			indiv_repro = (int)repro_rate_floor;
		}
		indiv.UpdateReproRate(indiv_repro);
	}
}

void Patch::UpdateIndivSurvRate(double SurvRateUL, double AgeStandard, double CostRate){
	for (Individual& indiv: _Individual){
		double IndivSurvRate = SurvRateUL*exp(-indiv.GetAge()/AgeStandard);
		indiv.UpdateSurvRate(IndivSurvRate);
	}
}

void Patch::UpdateAlive(){
	for (int i = 0; i < _Individual.size(); i++){
		if (!RG.RBern(_Individual[i].GetSurvRate())){
			_Individual.erase(_Individual.begin()+i);
			i--;
		}
	}
}

vector<double> Patch::GetOffspring(){
	vector<double> Offspring;
	for (Individual& indiv: _Individual){
		vector<double> tmp(indiv.GetReproRate(), indiv.GetCoopDeg());
		Offspring.insert(Offspring.end(), tmp.begin(), tmp.end());
	}
	return Offspring;
}

PopProcess::PopProcess(int OutputType, double CoopEfficiency, double ResMean, double ResHalfVarRange, double CostRate, double InitCoopProp, int Replic, int Span, \
					   bool Sociality){
    // Population state
    _PopSizeUL			= 1000000;
	_PopSize			= 300;
    _PatchNum			= 529;
	_InitCoopProp		= InitCoopProp;
	if (Sociality){
		_CoopProp		= InitCoopProp;
	}else{
		_CoopProp		= 0.0;
	}

    // Population structure
	_Patch = vector<Patch>(_PatchNum);

	// Resource consumption
	_ResMean			= ResMean;
	_ResHalfVarRange	= ResHalfVarRange;
	_CoopEfficiency		= CoopEfficiency;
    _MaxIncreRate		= 40;
	_MetabolicConsump	= 1.0;

	// Reproduction
    _CostRate			= CostRate;
    _HalfConst			= 10;
    _ReproMax			= 5.0;
	if (Sociality){
		_Heritability	= 0.999;
	}else{
		_Heritability	= 1.0;
	}

	// Survival rate
	_AgeStandard		= 2.0;
    _SurvRateUL			= 0.7;

    // For convenience of data computation
	_Length				= 23;
    _Span				= Span;
	_Replic				= Replic;
	_OutputType			= OutputType;

	// to initialize population
	int patch_id;
	for (int i = 0; i < _PopSize; i++){
		patch_id = RG.SampleInt(0, _PatchNum);
		if (i < _PopSize*_CoopProp){
			_Patch[patch_id].AddIndividual(patch_id, -1.0, 0);
		}else{
			_Patch[patch_id].AddIndividual(patch_id, 0.0, 0);
		}
	}
	double fluc_res = RG.RUnif(_ResMean-_ResHalfVarRange, _ResMean+_ResHalfVarRange);
	for (Patch& patch: _Patch){
		patch.UpdateResource(fluc_res, _CoopEfficiency, _MaxIncreRate);
	}
	ComputePopCoopData();
}

PopProcess::~PopProcess(){}

void PopProcess::OffspringDisperse(){
	int patch_id;
	for (int i = 0; i < _PatchNum; i++){
		vector<double> Offspring = _Patch[i].GetOffspring();
		for (double parent_trait: Offspring){
			patch_id = i;
			int dir = RG.R2DGaussian();
			switch (dir){
				case 0:{
					if ((i >= _Length*2) && (i%_Length >= 2)){ patch_id = (i/_Length-2)*_Length + i%_Length-2;	}
				}break;
				case 1:{
					if ((i >= _Length*2) && (i%_Length >= 1)){ patch_id = (i/_Length-2)*_Length + i%_Length-1;	}
				}break;
				case 2:{
					if (i >= _Length*2){ patch_id = (i/_Length-2)*_Length + i%_Length;	}
				}break;
				case 3:{
					if ((i >= _Length*2) && (i%_Length <= _Length-2)){ patch_id = (i/_Length-2)*_Length + i%_Length+1;	}
				}break;
				case 4:{
					if ((i >= _Length*2) && (i%_Length <= _Length-3)){ patch_id = (i/_Length-2)*_Length + i%_Length+2;	}
				}break;
				case 5:{
					if ((i >= _Length) && (i%_Length >= 2)){ patch_id = (i/_Length-1)*_Length + i%_Length-2;	}
				}break;
				case 6:{
					if ((i >= _Length) && (i%_Length >= 1)){ patch_id = (i/_Length-1)*_Length + i%_Length-1;	}
				}break;
				case 7:{
					if (i >= _Length){ patch_id = (i/_Length-1)*_Length + i%_Length;	}
				}break;
				case 8:{
					if ((i >= _Length) && (i%_Length <= _Length-2)){ patch_id = (i/_Length-1)*_Length + i%_Length+1;	}
				}break;
				case 9:{
					if ((i >= _Length) && (i%_Length <= _Length-3)){ patch_id = (i/_Length-1)*_Length + i%_Length+2;	}
				}break;
				case 10:{
					if (i%_Length >= 2){ patch_id = i-2;	}
				}break;
				case 11:{
					if (i%_Length >= 1){ patch_id = i-1;	}
				}break;
				case 12:{
					patch_id = i;
				}break;
				case 13:{
					if (i%_Length <= _Length-2){ patch_id = i+1;	}
				}break;
				case 14:{
					if (i%_Length <= _Length-3){ patch_id = i+2;	}
				}break;
				case 15:{
					if ((i <= _PatchNum-_Length-1) && (i%_Length >= 2)){ patch_id = (i/_Length+1)*_Length + i%_Length-2;	}
				}break;
				case 16:{
					if ((i <= _PatchNum-_Length-1) && (i%_Length >= 1)){ patch_id = (i/_Length+1)*_Length + i%_Length-1;	}
				}break;
				case 17:{
					if (i <= _PatchNum-_Length-1){ patch_id = (i/_Length+1)*_Length + i%_Length;	}
				}break;
				case 18:{
					if ((i <= _PatchNum-_Length-1) && (i%_Length <= _Length-2)){ patch_id = (i/_Length+1)*_Length + i%_Length+1;	}
				}break;
				case 19:{
					if ((i <= _PatchNum-_Length-1) && (i%_Length <= _Length-3)){ patch_id = (i/_Length+1)*_Length + i%_Length+2;	}
				}break;
				case 20:{
					if ((i <= _PatchNum-_Length*2-1) && (i%_Length >= 2)){ patch_id = (i/_Length+2)*_Length + i%_Length-2;	}
				}break;
				case 21:{
					if ((i <= _PatchNum-_Length*2-1) && (i%_Length >= 1)){ patch_id = (i/_Length+2)*_Length + i%_Length-1;	}
				}break;
				case 22:{
					if (i <= _PatchNum-_Length*2-1){ patch_id = (i/_Length+2)*_Length + i%_Length;	}
				}break;
				case 23:{
					if ((i <= _PatchNum-_Length*2-1) && (i%_Length <= _Length-2)){ patch_id = (i/_Length+2)*_Length + i%_Length+1;	}
				}break;
				case 24:{
					if ((i <= _PatchNum-_Length*2-1) && (i%_Length <= _Length-3)){ patch_id = (i/_Length+2)*_Length + i%_Length+2;	}
				}break;
			}
			double offspring_trait = parent_trait;
			if (!RG.RBern(_Heritability)){
				if (parent_trait != 0.0){
					offspring_trait = 0.0;
				}else{
					offspring_trait = RG.RandDeg();
				}
			}
			_Patch[patch_id].AddIndividual(patch_id, offspring_trait, 0);
		}
	}
}

void PopProcess::ErrorHandling1(){
	_TotalCoopNum   = 0;
	_CoopProp       = -1.0;
	_AverCoopDeg    = -1.0;	
}

void PopProcess::ErrorHandling2(){
    _PopSize        = -1;
	_TotalCoopNum   = -1;
	_CoopProp       = -1.0;
	_AverCoopDeg    = -1.0;
}

void PopProcess::EnvChange(double ResMeanOffset, double ResHalfVarRangeOffset){
	_Heritability		= 1.0;
	_ResMean			= _ResMean + ResMeanOffset;
	_ResHalfVarRange	= _ResHalfVarRange + ResHalfVarRangeOffset;
}

void PopProcess::ComputePopCoopData(){
	_TotalCoopNum = 0;
	_AverCoopDeg  = 0.0;
	for (Patch& patch: _Patch){
		patch.UpdateCoopNum();
		patch.UpdateCoopDegSum();
		_TotalCoopNum = _TotalCoopNum + patch.GetCoopNum();
		_AverCoopDeg  = _AverCoopDeg  + patch.GetCoopDegSum();
	}
	_CoopProp    = double(_TotalCoopNum)/double(_PopSize);
    _AverCoopDeg = _AverCoopDeg/double(_PopSize);
}

void PopProcess::ComputeTimeSeriesData(int Time){
	cout << _CoopEfficiency << "," << _CostRate << "," << _ResMean << "," << 2*_ResHalfVarRange << "," << _Replic << "," << Time+1 << "," \
		 << _PopSize << "," << _TotalCoopNum << "," << _PopSize-_TotalCoopNum << "," << _CoopProp << "," << _AverCoopDeg << "," << _InitCoopProp;
	
	for (int var_type = 0; var_type < 4; var_type++){
		for (Patch& patch: _Patch){
			cout << ",";
			switch (var_type)
			{
				case 0:{
					cout << patch.GetSize();
				}break;
				case 1:{
					cout << patch.GetCoopNum();
				}break;
				case 2:{
					cout << patch.GetCoopDegSum();
				}break;
				case 3:{
					cout << patch.GetFlucRes();
				}break;
			}
		}
	}
	cout << "\n";
}

Simulation::Simulation(int OutputType, double ResMean, double ResHalfVarRange, double ResMeanOffset, double ResHalfVarRangeOffset, double CoopEfficiency, \
					   double CostRate, double InitCoopProp, int EnvChangeTime, int EndTime, int InitReplic, int ReplicNum, int Span, bool Sociality){
	_OutputType				= OutputType;
	_EnvChangeTime			= EnvChangeTime;
	_EndTime				= EndTime;
	_InitReplic				= InitReplic;
	_ReplicNum				= ReplicNum;
	_Span					= Span;
	_CoopEfficiency			= CoopEfficiency;
	_ResMean				= ResMean;
	_ResHalfVarRange		= ResHalfVarRange;
	_ResMeanOffset			= ResMeanOffset;
	_ResHalfVarRangeOffset	= ResHalfVarRangeOffset;
	_CostRate				= CostRate;
	_Sociality			    = Sociality;
	_InitCoopProp			= InitCoopProp;
}

void Simulation::ProcessShunt(int OutputType){
	switch (OutputType)
	{
		case 1:{
			PopFinalState();
		}break;
		case 2:{
			PopTimeSeries();
		}break;
	}
}

void Simulation::PopFinalState(){
	for (int i = 0; i < _ReplicNum; i++){
		PopProcess PP(_OutputType, _CoopEfficiency, _ResMean, _ResHalfVarRange, _CostRate, _InitCoopProp, i, _Span, _Sociality);
		PP.SystemUpdate(0, _EnvChangeTime);
		cout << PP.GetPopSize() << "," << PP.GetTotalCoopNum() << "," << PP.GetPopSize()-PP.GetTotalCoopNum() << "," << PP.GetCoopProp() << "," << PP.GetAverCoopDeg();
		PP.EnvChange(_ResMeanOffset, _ResHalfVarRangeOffset);
		PP.SystemUpdate(_EnvChangeTime, _EndTime);
		cout << "," << _CoopEfficiency << "," << _CostRate << "," << _ResMean+_ResMeanOffset << "," << 2*(_ResHalfVarRange+_ResHalfVarRangeOffset);
        if (_Sociality){
			cout << ",Social,";
		}else{
			cout << ",Nonsocial,";
		}
		cout << _InitReplic+i << "," << PP.GetPopSize() << "," << PP.GetTotalCoopNum() << "," << PP.GetPopSize()-PP.GetTotalCoopNum() << "," \
			 << PP.GetCoopProp() << "," << PP.GetAverCoopDeg()  << "," << _InitCoopProp;
		vector<Patch> patches = PP.GetPatch();
		for (int var_type = 0; var_type < 4; var_type++){
			for (Patch& patch: patches){
				cout << ",";
				switch (var_type)
				{
					case 0:{
						cout << patch.GetSize();
					}break;
					case 1:{
						cout << patch.GetCoopNum();
					}break;
					case 2:{
						cout << patch.GetCoopDegSum();
					}break;
					case 3:{
						cout << patch.GetFlucRes();
					}break;
				}
			}
		}
		cout << "\n";
	}
}

void Simulation::PopTimeSeries(){
	for (int i = 0; i < _ReplicNum; i++){
		PopProcess PP(_OutputType, _CoopEfficiency, _ResMean, _ResHalfVarRange, _CostRate, _InitCoopProp, i, _Span, _Sociality);
        cout << _CoopEfficiency << "," << _CostRate << "," << _ResMean << "," << 2*_ResHalfVarRange << "," << _InitReplic+i << ",0," << PP.GetPopSize() << "," \
			 << PP.GetTotalCoopNum() << "," << PP.GetPopSize()-PP.GetTotalCoopNum() << "," << PP.GetCoopProp() << "," << PP.GetAverCoopDeg() << "," << _InitCoopProp;
		vector<Patch> patches = PP.GetPatch();
		for (int var_type = 0; var_type < 4; var_type++){
			for (Patch& patch: patches){
				cout << ",";
				switch (var_type)
				{
					case 0:{
						cout << patch.GetSize();
					}break;
					case 1:{
						cout << patch.GetCoopNum();
					}break;
					case 2:{
						cout << patch.GetCoopDegSum();
					}break;
					case 3:{
						cout << patch.GetFlucRes();
					}break;
				}
			}
		}
		cout << "\n";
		PP.SystemUpdate(0, _EnvChangeTime);
		PP.EnvChange(_ResMeanOffset, _ResHalfVarRangeOffset);
		PP.SystemUpdate(_EnvChangeTime, _EndTime);
	}
}