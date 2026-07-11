#include "PMTestActor.h"

APMTestActor::APMTestActor()
{
	PrimaryActorTick.bCanEverTick = false;
	TestLabel = TEXT("ProyectoMemoria C++/Blueprint link OK");
}

void APMTestActor::RunTestPing()
{
	OnTestPing();
}
