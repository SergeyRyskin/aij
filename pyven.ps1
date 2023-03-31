function Get-TerminalWidth() {
    $terminalWidth = (Get-Host).UI.RawUI.WindowSize.Width
    Write-Output $terminalWidth
}

function Test-TerminalWidth($expected) {
    $actual = Get-TerminalWidth
    assert {$actual -eq $expected}
}

function Get-TerminalHeight($expected) {
    $terminalHeight = (Get-Host).UI.RawUI.WindowSize.Height
    Write-Output $terminalHeight
}

function Test-TerminalHeight($expected) {
    $actual = Get-TerminalHeight
    assert {$actual -eq $expected}
}

function Get-TerminalSize() {
    $terminalSize = (Get-Host).UI.RawUI.WindowSize
    Write-Output $terminalSize
}

function Test-TerminalSize($expectedWidth, $expectedHeight) {
    Test-TerminalWidth $expectedWidth -and Test-TerminalHeight $expectedHeight
}

function Get-CurrentDirectory() {
    $currentDirectory = Get-Location
    Write-Output $currentDirectory
}

function Test-CurrentDirectory($expected) {
    $actual = Get-CurrentDirectory
    assert {$actual -eq $expected}
}

function Print-Separator($Title, $ForegroundColor = "Green") {

    $titleLength = $Title.Length
    $titleLengthHalf = [Math]::Floor($titleLength / 2)

    $terminalLength = Get-TerminalWidth
    $terminalLengthHalf = [Math]::Floor($terminalLength / 2) - $titleLengthHalf - 1
    $separator = ""

    # Print the first part of the separator
    for ($i = 0; $i -lt $terminalLengthHalf; $i++) {
        $separator += "#"
    }

    # Print the title
    $separator += " $Title "

    # Print the second part of the separator
    for ($i = 0; $i -lt $terminalLengthHalf; $i++) {
        $separator += "#"
    }

    Write-Host $separator -ForegroundColor $ForegroundColor
}

function Test-Separator($expected) {
    $actual = Print-Separator
    assert {$actual -eq $expected}
}

function Log-FunctionEvent() {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [Parameter(Mandatory = $true)]
        [string]$FunctionName
    )
    # Separator line with # character and function name
    Print-Separator $FunctionName -ForegroundColor "Green"
    Write-Host $Message -ForegroundColor Green
}

function Log-FunctionSuccess() {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [Parameter(Mandatory = $true)]
        [string]$FunctionName
    )
    Print-Separator $FunctionName -ForegroundColor "Green"
    Write-Host $Message -ForegroundColor Green
}

function Log-FunctionError() {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [Parameter(Mandatory = $true)]
        [string]$FunctionName
    )
    Print-Separator $FunctionName -ForegroundColor "Red"
    Write-Host $Message -ForegroundColor Red
}

function Test-FunctionError($expected) {
    $actual = Log-FunctionError
    assert {$actual -eq $expected}
}

function Log-FunctionWarning() {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        [Parameter(Mandatory = $true)]
        [string]$FunctionName
    )
    Print-Separator $FunctionName -ForegroundColor "Yellow"
    Write-Host $Message -ForegroundColor Yellow
}

function Test-FunctionWarning($expected) {
    $actual = Log-FunctionWarning
    assert {$actual -eq $expected}
}

function Get-PomPyXml() {
    Log-FunctionEvent -Message "Getting pom.xml" -FunctionName "Get-PomPyXml"
    $pom = [xml](Get-Content pompy.xml)
    Write-Output $pom
}

function Test-PomPyXml($expected) {
    $actual = Get-PomPyXml
    assert {$actual -eq $expected}
}

function Get-PomPyVersion() {
    Log-FunctionEvent -Message "Getting pom.xml version" -FunctionName "Get-PomPyVersion"
    $pom = Get-PomPyXml
    Write-Output $pom.project.version
}

function Test-PomPyVersion($expected) {
    $actual = Get-PomPyVersion
    assert {$actual -eq $expected}
}

function Get-PomPyArtifactId() {
    Log-FunctionEvent -Message "Getting pom.xml artifactId" -FunctionName "Get-PomPyArtifactId"
    $pom = Get-PomPyXml
    Write-Output $pom.project.artifactId
}

function Test-PomPyArtifactId($expected) {
    $actual = Get-PomPyArtifactId
    assert {$actual -eq $expected}
}

function Get-PomPyGroupId() {
    Log-FunctionEvent -Message "Getting pom.xml groupId" -FunctionName "Get-PomPyGroupId"
    $pom = Get-PomPyXml
    Write-Output $pom.project.groupId
}

function Test-PomPyGroupId($expected) {
    $actual = Get-PomPyGroupId
    assert {$actual -eq $expected}
}

function Get-PomPyName() {
    Log-FunctionEvent -Message "Getting pom.xml name" -FunctionName "Get-PomPyName"
    $pom = Get-PomPyXml
    Write-Output $pom.project.name
}

function Test-PomPyName($expected) {
    $actual = Get-PomPyName
    assert {$actual -eq $expected}
}

function Get-PomPyDescription() {
    Log-FunctionEvent -Message "Getting pom.xml description" -FunctionName "Get-PomPyDescription"
    $pom = Get-PomPyXml
    Write-Output $pom.project.description
}

function Test-PomPyDescription($expected) {
    $actual = Get-PomPyDescription
    assert {$actual -eq $expected}
}

function Get-PomPyUrl() {
    Log-FunctionEvent -Message "Getting pom.xml url" -FunctionName "Get-PomPyUrl"
    $pom = Get-PomPyXml
    Write-Output $pom.project.url
}

function Test-PomPyUrl($expected) {
    $actual = Get-PomPyUrl
    assert {$actual -eq $expected}
}

function Get-PomPyPackaging() {
    Log-FunctionEvent -Message "Getting pom.xml packaging" -FunctionName "Get-PomPyPackaging"
    $pom = Get-PomPyXml
    Write-Output $pom.project.packaging
}

function Test-PomPyPackaging($expected) {
    $actual = Get-PomPyPackaging
    assert {$actual -eq $expected}
}

function Get-PomPyInceptionYear() {
    Log-FunctionEvent -Message "Getting pom.xml inceptionYear" -FunctionName "Get-PomPyInceptionYear"
    $pom = Get-PomPyXml
    Write-Output $pom.project.inceptionYear
}

function Test-PomPyInceptionYear($expected) {
    $actual = Get-PomPyInceptionYear
    assert {$actual -eq $expected}
}

function Get-PomPyOrganization() {
    Log-FunctionEvent -Message "Getting pom.xml organization" -FunctionName "Get-PomPyOrganization"
    $pom = Get-PomPyXml
    Write-Output $pom.project.organization
}

function Test-PomPyOrganization($expected) {
    $actual = Get-PomPyOrganization
    assert {$actual -eq $expected}
}

function Get-PomPyOrganizationName() {
    Log-FunctionEvent -Message "Getting pom.xml organization name" -FunctionName "Get-PomPyOrganizationName"
    $pom = Get-PomPyXml
    Write-Output $pom.project.organization.name
}

function Test-PomPyOrganizationName($expected) {
    $actual = Get-PomPyOrganizationName
    assert {$actual -eq $expected}
}

function Get-PomPyOrganizationUrl() {
    Log-FunctionEvent -Message "Getting pom.xml organization url" -FunctionName "Get-PomPyOrganizationUrl"
    $pom = Get-PomPyXml
    Write-Output $pom.project.organization.url
}

function Test-PomPyOrganizationUrl($expected) {
    $actual = Get-PomPyOrganizationUrl
    assert {$actual -eq $expected}
}

function Get-PomPyLicense() {
    Log-FunctionEvent -Message "Getting pom.xml license" -FunctionName "Get-PomPyLicense"
    $pom = Get-PomPyXml
    Write-Output $pom.project.licenses.license
}

function Test-PomPyLicense($expected) {
    $actual = Get-PomPyLicense
    assert {$actual -eq $expected}
}

function Get-PomPyLicenseName() {
    Log-FunctionEvent -Message "Getting pom.xml license name" -FunctionName "Get-PomPyLicenseName"
    $pom = Get-PomPyXml
    Write-Output $pom.project.licenses.license.name
}

function Test-PomPyLicenseName($expected) {
    $actual = Get-PomPyLicenseName
    assert {$actual -eq $expected}
}

function Get-PomPyLicenseUrl() {
    Log-FunctionEvent -Message "Getting pom.xml license url" -FunctionName "Get-PomPyLicenseUrl"
    $pom = Get-PomPyXml
    Write-Output $pom.project.licenses.license.url
}

function Test-PomPyLicenseUrl($expected) {
    $actual = Get-PomPyLicenseUrl
    assert {$actual -eq $expected}
}

function Get-PomPyLicenseDistribution() {
    Log-FunctionEvent -Message "Getting pom.xml license distribution" -FunctionName "Get-PomPyLicenseDistribution"
    $pom = Get-PomPyXml
    Write-Output $pom.project.licenses.license.distribution
}

function Test-PomPyLicenseDistribution($expected) {
    $actual = Get-PomPyLicenseDistribution
    assert {$actual -eq $expected}
}

function Get-PomPyLicenseComments() {
    Log-FunctionEvent -Message "Getting pom.xml license comments" -FunctionName "Get-PomPyLicenseComments"
    $pom = Get-PomPyXml
    Write-Output $pom.project.licenses.license.comments
}

function Test-PomPyLicenseComments($expected) {
    $actual = Get-PomPyLicenseComments
    assert {$actual -eq $expected}
}

function Get-PomPyScm() {
    Log-FunctionEvent -Message "Getting pom.xml scm" -FunctionName "Get-PomPyScm"
    $pom = Get-PomPyXml
    Write-Output $pom.project.scm
}

function Test-PomPyScm($expected) {
    $actual = Get-PomPyScm
    assert {$actual -eq $expected}
}

function Get-PomPyScmConnection() {
    Log-FunctionEvent -Message "Getting pom.xml scm connection" -FunctionName "Get-PomPyScmConnection"
    $pom = Get-PomPyXml
    Write-Output $pom.project.scm.connection
}

function Test-PomPyScmConnection($expected) {
    $actual = Get-PomPyScmConnection
    assert {$actual -eq $expected}
}

function Get-PomPyScmDeveloperConnection() {
    Log-FunctionEvent -Message "Getting pom.xml scm developerConnection" -FunctionName "Get-PomPyScmDeveloperConnection"
    $pom = Get-PomPyXml
    Write-Output $pom.project.scm.developerConnection
}

function Test-PomPyScmDeveloperConnection($expected) {
    $actual = Get-PomPyScmDeveloperConnection
    assert {$actual -eq $expected}
}

function Get-PomPyScmUrl() {
    Log-FunctionEvent -Message "Getting pom.xml scm url" -FunctionName "Get-PomPyScmUrl"
    $pom = Get-PomPyXml
    Write-Output $pom.project.scm.url
}

function Test-PomPyScmUrl($expected) {
    $actual = Get-PomPyScmUrl
    assert {$actual -eq $expected}
}

function Get-PomPyScmTag() {
    Log-FunctionEvent -Message "Getting pom.xml scm tag" -FunctionName "Get-PomPyScmTag"
    $pom = Get-PomPyXml
    Write-Output $pom.project.scm.tag
}

function Test-PomPyScmTag($expected) {
    $actual = Get-PomPyScmTag
    assert {$actual -eq $expected}
}

function Get-PomPyIssueManagement() {
    Log-FunctionEvent -Message "Getting pom.xml issueManagement" -FunctionName "Get-PomPyIssueManagement"
    $pom = Get-PomPyXml
    Write-Output $pom.project.issueManagement
}

function Test-PomPyIssueManagement($expected) {
    $actual = Get-PomPyIssueManagement
    assert {$actual -eq $expected}
}

function Get-PomPyIssueManagementSystem() {
    Log-FunctionEvent -Message "Getting pom.xml issueManagement system" -FunctionName "Get-PomPyIssueManagementSystem"
    $pom = Get-PomPyXml
    Write-Output $pom.project.issueManagement.system
}

function Test-PomPyIssueManagementSystem($expected) {
    $actual = Get-PomPyIssueManagementSystem
    assert {$actual -eq $expected}
}

function Get-PomPyIssueManagementUrl() {
    Log-FunctionEvent -Message "Getting pom.xml issueManagement url" -FunctionName "Get-PomPyIssueManagementUrl"
    $pom = Get-PomPyXml
    Write-Output $pom.project.issueManagement.url
}

function Test-PomPyIssueManagementUrl($expected) {
    $actual = Get-PomPyIssueManagementUrl
    assert {$actual -eq $expected}
}

function Get-PomPyCiManagement() {
    Log-FunctionEvent -Message "Getting pom.xml ciManagement" -FunctionName "Get-PomPyCiManagement"
    $pom = Get-PomPyXml
    Write-Output $pom.project.ciManagement
}

function Test-PomPyCiManagement($expected) {
    $actual = Get-PomPyCiManagement
    assert {$actual -eq $expected}
}

function Get-PomPyCiManagementSystem() {
    Log-FunctionEvent -Message "Getting pom.xml ciManagement system" -FunctionName "Get-PomPyCiManagementSystem"
    $pom = Get-PomPyXml
    Write-Output $pom.project.ciManagement.system
}

function Test-PomPyCiManagementSystem($expected) {
    $actual = Get-PomPyCiManagementSystem
    assert {$actual -eq $expected}
}

function Get-PomPyCiManagementUrl() {
    Log-FunctionEvent -Message "Getting pom.xml ciManagement url" -FunctionName "Get-PomPyCiManagementUrl"
    $pom = Get-PomPyXml
    Write-Output $pom.project.ciManagement.url
}

function Test-PomPyCiManagementUrl($expected) {
    $actual = Get-PomPyCiManagementUrl
    assert {$actual -eq $expected}
}

function Get-Dependencies() {
    Log-FunctionEvent -Message "Getting pom.xml dependencies" -FunctionName "Get-Dependencies"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency
}

function Test-Dependencies($expected) {
    $actual = Get-Dependencies
    assert {$actual -eq $expected}
}

function Get-Dependency($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency" -FunctionName "Get-Dependency"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency }
}

function Test-Dependency($dependency, $expected) {
    $actual = Get-Dependency $dependency
    assert {$actual -eq $expected}
}

function Get-DependencyVersion($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency version" -FunctionName "Get-DependencyVersion"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty version
}

function Test-DependencyVersion($dependency, $expected) {
    $actual = Get-DependencyVersion $dependency
    assert {$actual -eq $expected}
}

function Get-DependencyGroupId($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency groupId" -FunctionName "Get-DependencyGroupId"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty groupId
}

function Test-DependencyGroupId($dependency, $expected) {
    $actual = Get-DependencyGroupId $dependency
    assert {$actual -eq $expected}
}

function Get-DependencyArtifactId($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency artifactId" -FunctionName "Get-DependencyArtifactId"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty artifactId
}

function Test-DependencyArtifactId($dependency, $expected) {
    $actual = Get-DependencyArtifactId $dependency
    assert {$actual -eq $expected}
}

function Get-DependencyScope($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency scope" -FunctionName "Get-DependencyScope"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty scope
}

function Test-DependencyScope($dependency, $expected) {
    $actual = Get-DependencyScope $dependency
    assert {$actual -eq $expected}
}

function Get-DependencyType($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency type" -FunctionName "Get-DependencyType"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty type
}

function Test-DependencyType($dependency, $expected) {
    $actual = Get-DependencyType $dependency
    assert {$actual -eq $expected}
}

function Get-DependencyClassifier($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency classifier" -FunctionName "Get-DependencyClassifier"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty classifier
}

function Test-DependencyClassifier($dependency, $expected) {
    $actual = Get-DependencyClassifier $dependency
    assert {$actual -eq $expected}
}

function Get-DependencySystemPath($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency systemPath" -FunctionName "Get-DependencySystemPath"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty systemPath
}

function Test-DependencySystemPath($dependency, $expected) {
    $actual = Get-DependencySystemPath $dependency
    assert {$actual -eq $expected}
}

function Get-DependencyExclusions($dependency) {
    Log-FunctionEvent -Message "Getting pom.xml dependency $dependency exclusions" -FunctionName "Get-DependencyExclusions"
    $pom = Get-PomPyXml
    Write-Output $pom.project.dependencies.dependency | Where-Object { $_.artifactId -eq $dependency } | Select-Object -ExpandProperty exclusions
}

function Test-DependencyExclusions($dependency, $expected) {
    $actual = Get-DependencyExclusions $dependency
    assert {$actual -eq $expected}
}

function Get-Build() {
    Log-FunctionEvent -Message "Getting pom.xml build" -FunctionName "Get-Build"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build
}

function Test-Build($expected) {
    $actual = Get-Build
    assert {$actual -eq $expected}
}

function Get-BuildDefaultGoal() {
    Log-FunctionEvent -Message "Getting pom.xml build defaultGoal" -FunctionName "Get-BuildDefaultGoal"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.defaultGoal
}

function Test-BuildDefaultGoal($expected) {
    $actual = Get-BuildDefaultGoal
    assert {$actual -eq $expected}
}

function Get-BuildSourceDirectory() {
    Log-FunctionEvent -Message "Getting pom.xml build sourceDirectory" -FunctionName "Get-BuildSourceDirectory"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.sourceDirectory
}

function Test-BuildSourceDirectory($expected) {
    $actual = Get-BuildSourceDirectory
    assert {$actual -eq $expected}
}

function Get-BuildPlugins() {
    Log-FunctionEvent -Message "Getting pom.xml build plugins" -FunctionName "Get-BuildPlugins"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins
}

function Test-BuildPlugins($expected) {
    $actual = Get-BuildPlugins
    assert {$actual -eq $expected}
}

function Get-BuildPlugin($plugin) {
    Log-FunctionEvent -Message "Getting pom.xml build plugin $plugin" -FunctionName "Get-BuildPlugin"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins.plugin | Where-Object { $_.artifactId -eq $plugin }
}

function Test-BuildPlugin($plugin, $expected) {
    $actual = Get-BuildPlugin $plugin
    assert {$actual -eq $expected}
}

function Get-BuildPluginVersion($plugin) {
    Log-FunctionEvent -Message "Getting pom.xml build plugin $plugin version" -FunctionName "Get-BuildPluginVersion"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins.plugin | Where-Object { $_.artifactId -eq $plugin } | Select-Object -ExpandProperty version
}

function Test-BuildPluginVersion($plugin, $expected) {
    $actual = Get-BuildPluginVersion $plugin
    assert {$actual -eq $expected}
}

function Get-BuildPluginGroupId($plugin) {
    Log-FunctionEvent -Message "Getting pom.xml build plugin $plugin groupId" -FunctionName "Get-BuildPluginGroupId"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins.plugin | Where-Object { $_.artifactId -eq $plugin } | Select-Object -ExpandProperty groupId
}

function Test-BuildPluginGroupId($plugin, $expected) {
    $actual = Get-BuildPluginGroupId $plugin
    assert {$actual -eq $expected}
}

function Get-BuildPluginArtifactId($plugin) {
    Log-FunctionEvent -Message "Getting pom.xml build plugin $plugin artifactId" -FunctionName "Get-BuildPluginArtifactId"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins.plugin | Where-Object { $_.artifactId -eq $plugin } | Select-Object -ExpandProperty artifactId
}

function Test-BuildPluginArtifactId($plugin, $expected) {
    $actual = Get-BuildPluginArtifactId $plugin
    assert {$actual -eq $expected}
}

function Get-BuildPluginExecutions() {
    Log-FunctionEvent -Message "Getting pom.xml build plugin executions" -FunctionName "Get-BuildPluginExecutions"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins.plugin.executions
}

function Test-BuildPluginExecutions($expected) {
    $actual = Get-BuildPluginExecutions
    assert {$actual -eq $expected}
}

function Get-BuildPluginExecution($plugin, $execution) {
    Log-FunctionEvent -Message "Getting pom.xml build plugin $plugin execution $execution" -FunctionName "Get-BuildPluginExecution"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins.plugin | Where-Object { $_.artifactId -eq $plugin } | Select-Object -ExpandProperty executions | Where-Object { $_.id -eq $execution }
}

function Test-BuildPluginExecution($plugin, $execution, $expected) {
    $actual = Get-BuildPluginExecution $plugin $execution
    assert {$actual -eq $expected}
}

function Get-MainClass() {
    Log-FunctionEvent -Message "Getting pom.xml mainClass" -FunctionName "Get-MainClass"
    $pom = Get-PomPyXml
    Write-Output $pom.project.build.plugins.plugin | Where-Object { $_.artifactId -eq 'pyven-assembly-plugin' } | Select-Object -ExpandProperty configuration | Select-Object -ExpandProperty archive | Select-Object -ExpandProperty manifest | Select-Object -ExpandProperty mainClass
}

function Test-MainClass($expected) {
    $actual = Get-MainClass
    assert {$actual -eq $expected}
}

function Get-Requirements() {

    Print-Separator -Message "Requirements" -FunctionName "Get-Requirements"

    Log-FunctionEvent -Message "Getting requirements.txt" -FunctionName "Get-Requirements"

    $dependencies = Get-Dependencies
    
    $requirements = @()
    
    $dependencies | ForEach-Object {
        $dependency = $_
        $dependencyName = $dependency.artifactId
        $dependencyVersion = $dependency.version
        if ($null -eq $dependencyVersion -or $dependencyVersion -eq 'LATEST' -or $dependencyVersion -eq 'RELEASE' -or $dependencyVersion -eq '') {
            $dependencyVersion = ''
            $dependencyName = $dependencyName.ToLower()
        }
        else {
            $dependencyVersion = "==$dependencyVersion"
        }

        $requirements += "$dependencyName$dependencyVersion"
    }

    Write-OutPut $requirements
}

function Test-Requirements($expected) {
    $actual = Get-Requirements
    assert {$actual -eq $expected}
}

function Write-Requirments() {

    Log-FunctionEvent -Message "Writing requirements.txt" -FunctionName "Write-Requirments"

    $requirements = Get-Requirements
    $requirements | Out-File -FilePath 'requirements.txt'

}

function Test-WriteRequirements() {
    Write-Requirments
    $actual = Get-Content -Path 'requirements.txt'
    $expected = Get-Requirements
    assert {$actual -eq $expected}
}

function Install-RequirementsUsingPip() {

    Log-FunctionEvent -Message "Installing requirements.txt" -FunctionName "Install-RequirementsUsingPip"

    $install = @()

    $requirements = Get-Requirements

    $requirements | ForEach-Object {
        $requirement = $_
        $requirementParts = $requirement.Split('==')
        $requirementName = $requirementParts[0]
        $requirementVersion = $requirementParts[1]

        if ($null -eq $requirementVersion -or $requirementVersion -eq '') {
            $requirementVersion = ''
        }
        else {
            $requirementVersion = "==$requirementVersion"
        }

        $requirementName = $requirementName.ToLower()

        $requirement = "$requirementName$requirementVersion"

        Write-OutPut "Installing $requirement"

        $install += pip install $requirement

    }

    # print installation if only successful, if failed skip it
    Write-OutPut $install
}

function Test-InstallRequirementsUsingPip() {
    Install-RequirementsUsingPip

    $requirements = Get-Requirements

    $requirements | ForEach-Object {
        $requirement = $_
        $requirementParts = $requirement.Split('==')
        $requirementName = $requirementParts[0]
        $requirementVersion = $requirementParts[1]

        if ($null -eq $requirementVersion -or $requirementVersion -eq '') {
            $requirementVersion = ''
        }
        else {
            $requirementVersion = "==$requirementVersion"
        }

        $requirementName = $requirementName.ToLower()

        $requirement = "$requirementName$requirementVersion"

        $actual = pip show $requirementName | Out-String
        $expected = "Name: $requirementName"
        assert {$actual -like $expected}
    }

}

function Install-RequirementsUsingConda() {

    Log-FunctionEvent -Message "Installing requirements.txt using conda" -FunctionName "Install-RequirementsUsingConda"

    # activate conda environment $condaEnv if it exists

    $install = @()

    $requirements = Get-Requirements

    $requirements | ForEach-Object {
        $requirement = $_
        $requirementParts = $requirement.Split('==')
        $requirementName = $requirementParts[0]
        $requirementVersion = $requirementParts[1]

        if ($null -eq $requirementVersion -or $requirementVersion -eq '') {
            $requirementVersion = ''
        }
        else {
            $requirementVersion = "==$requirementVersion"
        }

        $requirementName = $requirementName.ToLower()

        $requirement = "$requirementName$requirementVersion"

        Write-OutPut "Installing $requirement"

        $install += conda install $requirement

    }

    # print installation if only successful, if failed skip it
    Write-OutPut $install
}

function Test-InstallRequirementsUsingConda() {
    Install-RequirementsUsingConda

    $requirements = Get-Requirements

    $requirements | ForEach-Object {
        $requirement = $_
        $requirementParts = $requirement.Split('==')
        $requirementName = $requirementParts[0]
        $requirementVersion = $requirementParts[1]

        if ($null -eq $requirementVersion -or $requirementVersion -eq '') {
            $requirementVersion = ''
        }
        else {
            $requirementVersion = "==$requirementVersion"
        }

        $requirementName = $requirementName.ToLower()

        $requirement = "$requirementName$requirementVersion"

        $actual = conda list $requirementName | Out-String
        $expected = "$requirementName"
        assert {$actual -like $expected}
    }

}

function ConvertTo-PomPyXml() {

    Log-FunctionEvent -Message "Converting requirements.txt to pompy.xml" -FunctionName "ConvertTo-PomPyXml"

    $requirements = Get-Content -Path 'requirements.txt'

    $pom = Out-File -FilePath 'pompy.xml' -InputObject '<?xml version="1.0" encoding="UTF-8"?>' -Encoding UTF8
    $pom.project.dependencies = @()
    $pom.project.dependencies.dependency = @()

    $requirements | ForEach-Object {
        $requirement = $_
        $requirementParts = $requirement.Split('==')
        $requirementName = $requirementParts[0]
        $requirementVersion = $requirementParts[1]

        $pom.project.dependencies.dependency += @{
            groupId    = 'org.codesapienbe.python.deps'
            artifactId = $requirementName
            version    = $requirementVersion
            scope      = 'venv'
            type       = 'pip'
        }
    }

    Write-Output $pom
}

function Test-ConvertToPomPyXml() {
    $actual = ConvertTo-PomPyXml
    $expected = Get-Content -Path 'pompy.xml'
    assert {$actual -eq $expected}
}

function Write-PomPyXml($pom) {

    Log-FunctionEvent -Message "Writing pompy.xml" -FunctionName "Write-PomPyXml"

    $pom | Out-File -FilePath 'pompy.xml' -Encoding UTF8
}

function Start-StageClean() {

    Log-FunctionEvent -Message "Cleaning the project" -FunctionName "Start-StageClean"

    Write-OutPut 'Pyven cleaning the project...'

    if (Test-Path -Path 'venv') {

        if (Test-Path -Path 'venv\Scripts\deactivate') {
            Write-OutPut 'Pyven deactivating venv...'
            .\venv\Scripts\deactivate
            Write-OutPut 'Pyven venv deactivated!'
        }

        Remove-Item -Path 'venv' -Recurse -Force
    }

    if (Test-Path -Path 'target') {
        Remove-Item -Path 'target' -Recurse -Force
    }
    
    if (Test-Path "requirements.txt") {
        Remove-Item -Path 'requirements.txt' -Force
    }

    Write-OutPut 'Pyven cleaning done!'
}

function Test-StartStageClean() {
    Start-StageClean
    assert {!(Test-Path -Path 'venv')}
    assert {!(Test-Path -Path 'target')}
}

function Start-StageCreate() {

    Log-FunctionEvent -Message "Creating the project" -FunctionName "Start-StageCreate"

    Start-StageClean

    Log-Info 'Pyven creating the project...'

    if (Test-Path -Path 'venv') {
        Log-Info 'Pyven venv already exists!'
    }
    else {
        Log-Info 'Pyven creating venv...'
        python -m venv venv
        Log-Info 'Pyven venv created!'
    }

    if (Test-Path -Path 'target') {
        Log-Info 'Pyven target already exists!'
    }
    else {
        Log-Info 'Pyven creating target...'
        mkdir target
        Log-Info 'Pyven target created!'
    }

    if (Test-Path -Path 'requirements.txt') {
        Log-Info 'Pyven requirements.txt already exists!'
    }
    else {
        Log-Info 'Pyven creating requirements.txt...'
        Write-Requirments
        Log-Info 'Pyven requirements.txt created!'
    }

    $pompyXmlData = ConvertTo-PomPyXml
    $pomXmlFile = Write-PomPyXml $pompyXmlData

    Write-OutPut $pomXmlFile

    Log-Info 'Pyven creating done!'

    Write-Output Join-Path -Path $pwd -ChildPath 'venv\Scripts\activate' -ErrorAction SilentlyContinue
}

function Test-StartStageCreate() {
    Start-StageCreate
    assert {Test-Path -Path 'venv'}
    assert {Test-Path -Path 'target'}
    assert {Test-Path -Path 'requirements.txt'}
}

function Start-StageInit() {

    Log-FunctionEvent -Message "Initializing the project" -FunctionName "Start-StageInit"

    Write-OutPut 'Pyven initializing the project...'

    if (Test-Path -Path 'venv') {
        Write-OutPut 'Pyven venv already exists!'
    }
    else {
        Write-OutPut 'Pyven creating venv...'
        python -m venv venv
        Write-OutPut 'Pyven venv created!'
    }

    Write-OutPut 'Pyven initializing done!'

    Write-OutPut 'Pyven activating venv...'

    .\venv\Scripts\activate

    Write-OutPut 'Pyven venv activated!'
}

function Test-StartStageInit() {
    Start-StageInit
    assert {Test-Path -Path 'venv'}

    # make sure venv is activated 
    $pvenvCfg = Get-Content -Path 'venv\pyvenv.cfg'
    
    assert {$pvenvCfg -match 'home = .*venv'}
}

function Test-DependencyOnline() {
    
    Log-FunctionEvent -Message "Testing dependency online" -FunctionName "Test-DependencyOnline"
    
    $dependencyName = $args[0]
    $dependencyVersion = $args[1]
    
    $dependencyUrl = "https://pypi.org/pypi/$dependencyName/json"
    
    $dependencyData = Invoke-WebRequest -Uri $dependencyUrl -UseBasicParsing
    
    $dependencyData = $dependencyData.Content | ConvertFrom-Json
    
    $dependencyVersions = $dependencyData.releases.Keys
    
    $dependencyVersions | ForEach-Object {
        $dependencyVersion = $_
        if ($dependencyVersion -eq $dependencyVersion) {
            return $true
        }
    }
    
    return $false
}

function Test-DependencyOnlineNoVersion() {
    
    Log-FunctionEvent -Message "Testing dependency online no version" -FunctionName "Test-DependencyOnlineNoVersion"
    
    $dependencyName = $args[0]
    
    $dependencyUrl = "https://pypi.org/pypi/$dependencyName/json"
    
    $dependencyData = Invoke-WebRequest -Uri $dependencyUrl -UseBasicParsing
    
    $dependencyData = $dependencyData.Content | ConvertFrom-Json
    
    $dependencyVersions = $dependencyData.releases.Keys
    
    if ($dependencyVersions.Count -gt 0) {
        return $true
    }
    
    return $false
}

function Invoke-PipSearchPackage() {
    
    Log-FunctionEvent -Message "Invoking pip search package" -FunctionName "Invoke-PipSearchPackage"
    
    $dependencyName = $args[0]
    $result = pip search $dependencyName
    $result = $result | Select-String -Pattern "^\s*$dependencyName\s*"

    if ($result) {
        return $true
    }

    return $false
}

function Test-PipSearchPackage() {
    
    Log-FunctionEvent -Message "Testing pip search package" -FunctionName "Test-PipSearchPackage"
    
    $dependencyName = $args[0]
    $dependencyVersion = $args[1]
    
    $result = pip search $dependencyName
    $result = $result | Select-String -Pattern "^\s*$dependencyName\s*$dependencyVersion\s*"

    if ($result) {
        return $true
    }

    return $false
}


function Start-StageInstall() {

    Log-FunctionEvent -Message "Installing the project" -FunctionName "Start-StageInstall"

    Write-Requirments
    Install-RequirementsUsingPip
}

function Test-StartStageInstall() {
    Start-StageInstall
    assert {Test-Path -Path 'venv'}
    assert {Test-Path -Path 'target'}
    assert {Test-Path -Path 'requirements.txt'}
}

function Install-JupyterKernel() {

    Log-FunctionEvent -Message "Installing jupyter kernel" -FunctionName "Install-JupyterKernel"

    Log-Info 'Pyven installing jupyter kernel...'

    $kernelName = Read-Input -Message 'Kernel name' -DefaultValue 'venv'

    $kernelSpec = @{
        argv = @('python', '-m', 'ipykernel_launcher', '-f', '{connection_file}')
        display_name = $kernelName
        language = 'python'
    }

    $kernelSpec | ConvertTo-Json -Depth 10 | Out-File -FilePath 'kernel.json'

    $kernelSpecPath = Join-Path -Path $pwd -ChildPath 'kernel.json'

    python -m ipykernel install --user --name $kernelName --display-name $kernelName --specfile $kernelSpecPath

    Log-Info 'Pyven jupyter kernel installed!'
}

function Get-PyPomXML() {

    Log-FunctionEvent -Message "Getting py pom xml" -FunctionName "Get-PyPomXML"

    $pomXML = @'

    <?xml version="1.0" encoding="UTF-8"?>

    <project xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="pompy.xsd">
        
        <modelVersion>4.0.0</modelVersion>
    
        <groupId>be.ehb.postgradai</groupId>
        <artifactId>horse_survival</artifactId>
        <version>1.0.0</version>
        <name>horse_survival</name>
        <description>Python based machine learning project for horse survival</description>
        <url>https://github.com/yilmazchef/horse_survival</url>
        <packaging>pip</packaging>
    
        <properties>
            <python.version>3.11</python.version>
            <python.executable>python</python.executable>
        </properties>
    
        <dependencies>
    
            <!-- Pylint: Python code static checker -->
            <dependency>
                <artifactId>pylint</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- Pytest: Python unit testing framework -->
            <dependency>
                <artifactId>pytest</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- Pyinstaller: Python executable builder -->
            <dependency>
                <artifactId>pyinstaller</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- PEP8: Python code style checker -->
            <dependency>
                <artifactId>pep8</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- jupyter: Python notebook server -->
            <dependency>
                <artifactId>jupyter</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- nbconvert: Python notebook converter -->
            <dependency>
                <artifactId>nbconvert</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- NBFormat: Python notebook format library -->
            <dependency>
                <artifactId>nbformat</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- Numpy: Python scientific computing library -->
            <dependency>
                <artifactId>numpy</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- Pandas: Python data analysis library -->
            <dependency>
                <artifactId>pandas</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- scikit-learn: Python machine learning library -->
            <dependency>
                <artifactId>scikit-learn</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- Seaborn: Python data visualization library -->
            <dependency>
                <artifactId>seaborn</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- Matplotlib: Python plotting library -->
            <dependency>
                <artifactId>matplotlib</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- Plotly: Python plotting library -->
            <dependency>
                <artifactId>plotly</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
            <!-- PyWidgets: Python interactive widgets library -->
            <dependency>
                <artifactId>ipywidgets</artifactId>
                <groupId>org.codesapienbe.python.deps</groupId>
            </dependency>
    
        </dependencies>
    
        <build>
            <plugins>
                <plugin>
                    <groupId>org.codesapienbe.python.build</groupId>
                    <artifactId>python-maven-plugin</artifactId>
                    <version>1.0.0</version>
                    <configuration>
                        <source>${python.version}</source>
                        <target>${python.version}</target>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    
    </project>

'@

    return $pomXML

}

function Get-PyPomXSD(){

    Log-FunctionEvent -Message "Getting py pom xsd" -FunctionName "Get-PyPomXSD"

    $pomXSD = @'
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="project">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="modelVersion" type="xs:string" />
                <xs:element name="groupId" type="xs:string" />
                <xs:element name="artifactId" type="xs:string" />
                <xs:element name="version" type="xs:string" />
                <xs:element name="name" type="xs:string" />
                <xs:element name="description" type="xs:string" />
                <xs:element name="url" type="xs:string" />
                <xs:element name="packaging" type="xs:string" />
                <xs:element name="properties">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="python.version" type="xs:string" />
                            <xs:element name="python.executable" type="xs:string" />
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="dependencies">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="dependency" maxOccurs="unbounded">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="artifactId" type="xs:string" />
                                        <xs:element name="groupId" type="xs:string" />
                                    </xs:sequence>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="build">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="plugins">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="plugin">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:element name="groupId" type="xs:string" />
                                                    <xs:element name="artifactId" type="xs:string" />
                                                    <xs:element name="version" type="xs:string" />
                                                    <xs:element name="configuration">
                                                        <xs:complexType>
                                                            <xs:sequence>
                                                                <xs:element name="source"
                                                                    type="xs:string" />
                                                                <xs:element name="target"
                                                                    type="xs:string" />
                                                            </xs:sequence>
                                                        </xs:complexType>
                                                    </xs:element>
                                                </xs:sequence>
                                            </xs:complexType>
                                        </xs:element>
                                    </xs:sequence>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
'@

    return $pomXSD

}

function New-PythonProject() {

    Log-FunctionEvent -Message "Creating new python project" -FunctionName "New-PythonProject"

    param(
        [Parameter(Mandatory=$true)]
        [string]$projectName
    )

    $projectPath = Join-Path -Path $pwd -ChildPath $projectName

    if (Test-Path -Path $projectPath) {
        Log-Error "Project path already exists: $projectPath"
        return
    }

    New-Item -Path $projectPath -ItemType Directory
    $projectPath = Join-Path -Path $projectPath -ChildPath $projectName

    $pomXML = Get-PyPomXML -ProjectName $projectName
    $pomXML | Out-File -FilePath "$projectPath/pypom.xml" -Encoding UTF8

    $pomXSD = Get-PyPomXSD
    $pomXSD | Out-File -FilePath "$projectPath/pypom.xsd" -Encoding UTF8

    Log-FunctionSuccess -Message "Created new python project: $projectPath" -FunctionName "New-PythonProject"   

    return $projectPath

}

# get arguments from command line
$stages = $args

# if no arguments are passed, execute all stages
if ($stages.Count -eq 0) {
    $stages = @('clean', 'install')
}

Print-Separator -Message "Pyven started!" -ForegroundColor Yellow

# execute stages in order of appearance
$stages | ForEach-Object {
    $stage = $_

    switch ($stage) {
        'clean' {
            Start-StageClean
        }
        'create' {
            Start-StageCreate
        }
        'package' {
            Start-StageInit
        }
        'install' {
            Start-StageInit
            Start-StageInstall
            Install-JupyterKernel
        }
        'test' {
            Start-StageTest
        }
        default {
            Write-Error "Unknown stage: $stage"
        }
    }
}


Print-Separator -Message "Pyven finished!" -ForegroundColor Yellow
