#include "MagicalForestEnvironment.h"
#include "Engine/Engine.h"

AMagicalForestEnvironment::AMagicalForestEnvironment()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AMagicalForestEnvironment::BeginPlay()
{
    Super::BeginPlay();
    LoadEnvironmentFromJSON();
    ApplyEnvironmentSettings();
}

void AMagicalForestEnvironment::LoadEnvironmentFromJSON()
{
    // Load environment data from JSON
    UE_LOG(LogTemp, Warning, TEXT("Loading environment: %s"), *EnvironmentData.EnvironmentType);
}

void AMagicalForestEnvironment::ApplyEnvironmentSettings()
{
    // Apply environment settings to the world
    UE_LOG(LogTemp, Warning, TEXT("Applied environment settings for %s"), *EnvironmentData.Setting);
}