#include "llvm/ADT/APFloat.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Verifier.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/TargetParser/Host.h"

#include <string>
#include <iostream>


using namespace llvm;
using namespace llvm::sys;


static std::unique_ptr<LLVMContext> Context;


// è un pattern passare i moduli per puntatore?
void generate_addition_func(Type* type, const char* type_name, Module& mod, IRBuilder<>& builder) {
	const bool is_integer = type->isIntegerTy();
	const bool is_float = (
		type->isHalfTy()
		or type->isBFloatTy()
		or type->isFloatTy()
		or type->isDoubleTy()
	);
	assert(is_integer or is_float);

	// the API is sophisticated enough to allow initializer lists
	FunctionType *FT = FunctionType::get(type, { type, type }, false);
	Function *F = Function::Create( FT,
		Function::ExternalLinkage,
		Twine("add_", StringRef(type_name)),
		mod
	);
	Value* x = F->getArg(0);
	Value* y = F->getArg(1);

	BasicBlock *BB = BasicBlock::Create(*Context, "entry", F);
	builder.SetInsertPoint(BB);

	Value* val = nullptr;
	if (is_integer) {
		val = builder.CreateAdd(x, y);
	} else {
		val = builder.CreateFAdd(x, y);
	}
	builder.CreateRet(val);
}


int main() {
	Context = std::make_unique<LLVMContext>();
	InitializeAllTargetInfos();
	InitializeAllTargets();
	InitializeAllTargetMCs();
	InitializeAllAsmParsers();
	InitializeAllAsmPrinters();

	// BFloat is not enabled because not all targets support it
	//
	// a Module can be target independent, but its lowering must be target informed
	// this will spawn situations in which the lowering for some targets fail
	const std::vector<std::pair<Type*, const char*>> types = {
		{Type::getInt8Ty  (*Context), "i8"  },
		{Type::getInt16Ty (*Context), "i16" },
		{Type::getInt32Ty (*Context), "i32" },
		{Type::getInt64Ty (*Context), "i64" },
		{Type::getInt128Ty(*Context), "i128"},
		{Type::getHalfTy  (*Context), "half"},
		// {Type::getBFloatTy(*Context), "bf16"},
		{Type::getFloatTy (*Context), "f32" },
		{Type::getDoubleTy(*Context), "f64" },
	};

	const std::vector<const char*> triplets = {
		"arm-linux-gnueabihf",
		"aarch64-unknown-linux-gnu",
		"x86_64-pc-linux-gnu",
	};


	// builds a module that contains the implementations of addition
	// between different numeric types
	std::unique_ptr<Module> mod =
		std::make_unique<Module>("addition_module", *Context);
	std::unique_ptr<IRBuilder<>> builder =
		std::make_unique<IRBuilder<>>(*Context);

	for (auto [type, type_name] : types) {
		generate_addition_func(type, type_name, *mod, *builder);
	}

	// here I build once the pass manager which is responsible of
	//   * (not included yet) validating the module
	//   * converting the whole module to assembly

	std::string Error;
	for (const char* target_triple : triplets) {
		// future versions of llvm require a Triple object
		const Target* target = TargetRegistry::lookupTarget(target_triple, Error);
		if (!target) {
			errs() << Error;
			continue;
		}

		TargetOptions opz;
		TargetMachine* target_machine = target->createTargetMachine(
			target_triple,
			"generic",
			"",
			opz,
			Reloc::PIC_
		);

		// WARNING: this mutates the module, but I think it's necessary
		// the data layout controls endianness, alignment...
		mod->setDataLayout(target_machine->createDataLayout());


		// I want to save the assembly into my data structure, instead of file
		// I know the allocations are all over the place...
		SmallVector<char,0> asm_buffer;
		raw_svector_ostream asm_stream(asm_buffer);

		// the pass manager is specific to a target machine, it can't be hoisted
		// it will be responsible of:
		//   * (not included yet) validating the module
		//   * converting the whole module to assembly
		llvm::legacy::PassManager pass;
		if (target_machine->addPassesToEmitFile(
			pass,
			asm_stream,
			nullptr,
			llvm::CodeGenFileType::AssemblyFile)) {

			llvm::errs() << "TargetMachine " << target_triple << " can't emit a file of this type.\n";
			continue;
		}

		pass.run(*mod);

		std::string asm_string(asm_buffer.begin(), asm_buffer.end());
		errs() << asm_string << "\n";
	}

	return 0;
}
