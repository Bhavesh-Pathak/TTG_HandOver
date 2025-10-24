#include "CyberpunkCityEnvironment.h"
#include "Engine/Engine.h"

ACyberpunkCityEnvironment::ACyberpunkCityEnvironment()
{
    PrimaryActorTick.bCanEverTick = false;
}

void ACyberpunkCityEnvironment::BeginPlay()
{
    Super::BeginPlay();
    LoadEnvironmentFromJSON();
    ApplyEnvironmentSettings();
}

void ACyberpunkCityEnvironment::LoadEnvironmentFromJSON()
{
    // Load environment data from JSON
    UE_LOG(LogTemp, Warning, TEXT("Loading environment: %s"), *EnvironmentData.EnvironmentType);
}

void ACyberpunkCityEnvironment::ApplyEnvironmentSettings()
{
    // Apply environment settings to the world
    UE_LOG(LogTemp, Warning, TEXT("Applied environment settings for %s"), *EnvironmentData.Setting);
}