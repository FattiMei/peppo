#include "llvm/IR/Module.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Transforms/InstCombine/InstCombine.h"

#include <iostream>


using namespace llvm;


static std::unique_ptr<LLVMContext> Context;


std::unique_ptr<Module> mul_by_constant(int32_t c) {
	std::unique_ptr<Module> res = std::make_unique<Module>(
		"my_module",
		*Context
	);

	std::vector<Type*> signature{Type::getInt32Ty(*Context)};
	FunctionType *FT = FunctionType::get(
		Type::getInt32Ty(*Context),
		signature,
		false
	);

	// ma è un pattern che devo ogni volta guardare
	// se il risultato è null?
	Function *F = Function::Create(
		FT,
		Function::ExternalLinkage,
		"mul_by_constant",
		*res
	);

	auto Builder = std::make_unique<IRBuilder<>>(*Context);
	BasicBlock *BB = BasicBlock::Create(*Context, "entry", F);
	Builder->SetInsertPoint(BB);
	Builder->CreateRet(
		Builder->CreateMul(
			F->getArg(0),
			Builder->getInt32(c)
		)
	);

	return res;
}


std::unique_ptr<Module> div_by_constant(int32_t c) {
	std::unique_ptr<Module> res = std::make_unique<Module>(
		"my_module",
		*Context
	);

	std::vector<Type*> signature{Type::getInt32Ty(*Context)};
	FunctionType *FT = FunctionType::get(
		Type::getInt32Ty(*Context),
		signature,
		false
	);

	// ma è un pattern che devo ogni volta guardare
	// se il risultato è null?
	Function *F = Function::Create(
		FT,
		Function::ExternalLinkage,
		"div_by_constant",
		*res
	);

	auto Builder = std::make_unique<IRBuilder<>>(*Context);
	BasicBlock *BB = BasicBlock::Create(*Context, "entry", F);
	Builder->SetInsertPoint(BB);
	Builder->CreateRet(
		Builder->CreateSDiv(
			F->getArg(0),
			Builder->getInt32(c)
		)
	);

	return res;
}


int main() {
	Context = std::make_unique<LLVMContext>();

	// https://llvm.org/docs/NewPassManager.html
	LoopAnalysisManager LAM;
	FunctionAnalysisManager FAM;
	CGSCCAnalysisManager CGAM;
	ModuleAnalysisManager MAM;

	// Create the new pass manager builder.
	// Take a look at the PassBuilder constructor parameters for more
	// customization, e.g. specifying a TargetMachine or various debugging
	// options.
	PassBuilder PB;

	// Register all the basic analyses with the managers.
	PB.registerModuleAnalyses(MAM);
	PB.registerCGSCCAnalyses(CGAM);
	PB.registerFunctionAnalyses(FAM);
	PB.registerLoopAnalyses(LAM);
	PB.crossRegisterProxies(LAM, FAM, CGAM, MAM);

	ModulePassManager MPM;
	FunctionPassManager FPM;
	FPM.addPass(InstCombinePass());
	MPM.addPass(createModuleToFunctionPassAdaptor(std::move(FPM)));

	constexpr auto NMAX = 256;

	std::cout << "# Multiplication by constants\n"
		  << "numbers affected: ";
	for (int i = 0; i <= NMAX; ++i) {
		const auto mod = mul_by_constant(i);

		const PreservedAnalyses res = MPM.run(*mod, MAM);
		if (not res.areAllPreserved()) {
			std::cout << i << " ";
		}
	}
	std::cout << "\n\n";

	std::cout << "# Division by constants\n"
		  << "numbers affected: ";
	for (int i = 0; i <= NMAX; ++i) {
		const auto mod = div_by_constant(i);

		const PreservedAnalyses res = MPM.run(*mod, MAM);
		if (not res.areAllPreserved()) {
			std::cout << i << " ";
		}
	}
	std::cout << "\n";

	return 0;
}
