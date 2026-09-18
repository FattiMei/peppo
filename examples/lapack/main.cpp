#include "PeppoJIT.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Operator.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Instructions.h"
#include "llvm/AsmParser/Parser.h"
#include "llvm/Support/SourceMgr.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/Error.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Target/TargetMachine.h"
#include "llvm/Target/TargetOptions.h"
#include "llvm/TargetParser/Host.h"
#include <iostream>


using namespace llvm;
using namespace llvm::orc;


static std::unique_ptr<LLVMContext> Context;
static std::unique_ptr<llvm::orc::PeppoJIT> JIT;
static ExitOnError ExitOnErr;


bool check_only_loads_and_stores(Value *val) {
	for (Value::user_iterator i = val->user_begin(),
	                          e = val->user_end();
	                          i != e;
	                          ++i) {
		const StoreInst* store = dyn_cast<StoreInst>(*i);
		const LoadInst* load = dyn_cast<LoadInst>(*i);

		if (store == nullptr and load == nullptr) {
			return false;
		}
	}

	return true;
}


// for this particular implementation, I check that:
//   * no pointer arithmetic is done except for getelementptr
//   * %2, %3, %4 are used only by getelementptr and that pointers are only L/S
//
// this is the type of workflow that requires interactivity since we are
// exploring a new program transformation
bool check_assumptions(const Function* F) {
	Value* dl = F->getArg(2);
	Value*  d = F->getArg(3);
	Value* du = F->getArg(4);

	for (Value* diagonal : { dl, d, du }) {
		for (Value::user_iterator i = diagonal->user_begin(),
		                          e = diagonal->user_end();
		     i != e;
		     ++i) {
			GEPOperator* op = dyn_cast<GEPOperator>(*i);

			if (op == nullptr) {
				return false;
			}

			bool only_loads_and_stores =
				check_only_loads_and_stores(*i);

			if (not only_loads_and_stores) {
				return false;
			}
		}
	}

	return true;
}


int main() {
	Context = std::make_unique<LLVMContext>();
	InitializeNativeTarget();
	JIT = ExitOnErr(PeppoJIT::Create());

	// module loading from a LLVM assembly
	llvm::SMDiagnostic err;
	std::unique_ptr<llvm::Module> mod = llvm::parseAssemblyFile(
		LAPACK_IR_PATH,
		err,
		*Context
	);
	if (!mod) {
		err.print("IRParser", llvm::errs());
		return 1;
	}

	// I have made particular assumptions about the structure of
	// the function that solves tridiagonal systems
	//
	// Those assumptions will be exploited for a custom program
	// transformation later
	const std::string dgtsv_function_name = "dgtsv_";
	Function* dgtsv = mod->getFunction(
		dgtsv_function_name
	);
	assert(dgtsv != NULL);
	assert(check_assumptions(dgtsv));

	mod->setDataLayout(JIT->getDataLayout());
	ThreadSafeModule TSM(std::move(mod), std::move(Context));
	ExitOnErr(JIT->addModule(std::move(TSM)));

	auto DgtsvSymbol = ExitOnErr(
		JIT->lookup(dgtsv_function_name)
	);

	return 0;
}

