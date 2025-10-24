#include "CyberpunkCityPlayerController.h"
#include "Engine/Engine.h"

ACyberpunkCityPlayerController::ACyberpunkCityPlayerController()
{
    // Initialize player abilities
        PlayerAbilities.Add(TEXT("walk"));
    PlayerAbilities.Add(TEXT("run"));
    PlayerAbilities.Add(TEXT("jump"));
    PlayerAbilities.Add(TEXT("interact"));
}

void ACyberpunkCityPlayerController::BeginPlay()
{
    Super::BeginPlay();
    LoadPlayerSettings();
}

void ACyberpunkCityPlayerController::SetupInputComponent()
{
    Super::SetupInputComponent();
    // Setup input bindings here
}

bool ACyberpunkCityPlayerController::HasAbility(const FString& AbilityName) const
{
    return PlayerAbilities.Contains(AbilityName);
}

void ACyberpunkCityPlayerController::LoadPlayerSettings()
{
    UE_LOG(LogTemp, Warning, TEXT("Loaded player settings - Speed: %f, Jump: %f"), MovementSpeed, JumpHeight);
}