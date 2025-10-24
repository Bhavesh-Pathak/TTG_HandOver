#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "CyberpunkCityEnvironment.generated.h"

USTRUCT(BlueprintType)
struct FCyberpunkCityEnvironmentData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString EnvironmentType = TEXT("urban");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Setting = TEXT("A bustling city environment");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Lighting = TEXT("dynamic_lighting");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Weather = TEXT("clear");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Atmosphere = TEXT("mysterious");
};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API ACyberpunkCityEnvironment : public AActor
{
    GENERATED_BODY()

public:
    ACyberpunkCityEnvironment();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FCyberpunkCityEnvironmentData EnvironmentData;

public:
    UFUNCTION(BlueprintCallable, Category = "Environment")
    void LoadEnvironmentFromJSON();

    UFUNCTION(BlueprintCallable, Category = "Environment")
    void ApplyEnvironmentSettings();
};