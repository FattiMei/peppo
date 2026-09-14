#include "llvm/IR/Module.h"
#include "llvm/IR/IRBuilder.h"
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


int main() {
	Context = std::make_unique<LLVMContext>();

	const auto mod = mul_by_constant(10);
	mod->dump();

	return 0;
}
