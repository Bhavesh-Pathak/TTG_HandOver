#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Engine/DataTable.h"
#include "MagicalForestQuestSystem.generated.h"

UENUM(BlueprintType)
enum class EQuestType : uint8
{
    Main UMETA(DisplayName = "Main Quest"),
    Side UMETA(DisplayName = "Side Quest"),
    Optional UMETA(DisplayName = "Optional Quest")
};

UENUM(BlueprintType)
enum class EQuestStatus : uint8
{
    NotStarted UMETA(DisplayName = "Not Started"),
    InProgress UMETA(DisplayName = "In Progress"),
    Completed UMETA(DisplayName = "Completed"),
    Failed UMETA(DisplayName = "Failed")
};

USTRUCT(BlueprintType)
struct FMagicalForestQuestReward : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reward")
    int32 Experience = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reward")
    int32 Gold = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Reward")
    TArray<FString> Items;
};

USTRUCT(BlueprintType)
struct FMagicalForestQuest : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString QuestID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString QuestName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    EQuestType QuestType = EQuestType::Main;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Objective;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    TArray<FString> Requirements;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FMagicalForestQuestReward Rewards;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Location;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString EstimatedTime;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    EQuestStatus Status = EQuestStatus::NotStarted;
};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API AMagicalForestQuestSystem : public AActor
{
    GENERATED_BODY()

public:
    AMagicalForestQuestSystem();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest System")
    TArray<FMagicalForestQuest> Quests;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest System")
    TArray<FMagicalForestQuest> ActiveQuests;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest System")
    TArray<FMagicalForestQuest> CompletedQuests;

public:
    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool StartQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool CompleteQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool IsQuestActive(const FString& QuestID) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    bool IsQuestCompleted(const FString& QuestID) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    FMagicalForestQuest GetQuest(const FString& QuestID) const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    TArray<FMagicalForestQuest> GetActiveQuests() const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    TArray<FMagicalForestQuest> GetAvailableQuests() const;

    UFUNCTION(BlueprintCallable, Category = "Quest System")
    void LoadQuestsFromJSON();

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestStarted, const FMagicalForestQuest&, Quest);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestCompleted, const FMagicalForestQuest&, Quest);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestFailed, const FMagicalForestQuest&, Quest);

    UPROPERTY(BlueprintAssignable, Category = "Quest System")
    FOnQuestStarted OnQuestStarted;

    UPROPERTY(BlueprintAssignable, Category = "Quest System")
    FOnQuestCompleted OnQuestCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Quest System")
    FOnQuestFailed OnQuestFailed;
};